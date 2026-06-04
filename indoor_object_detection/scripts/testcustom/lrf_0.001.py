from ultralytics import YOLO
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# CONFIG
# ----------------------------
DATA_YAML = "dataset/merge_dataset_final/data.yaml"
MODEL = "custom_yolov8n1.yaml"
EPOCHS = 20
IMGSZ = 640
BATCH = 32
DEVICE = 0

PROJECT_DIR = "runs/testcustom"
RUN_NAME = "result_lrf_0.001_new"

# ----------------------------
# Train model
# ----------------------------
def train_model():
    model = YOLO(MODEL)

    results = model.train(
        data=DATA_YAML,
        epochs=EPOCHS,
        imgsz=IMGSZ,
        batch=BATCH,
        optimizer="SGD",
        device=DEVICE,
        pretrained=False,
        plots=True,
        project=PROJECT_DIR,
        name=RUN_NAME,
        save=True,
        val=True,
        momentum=0.97,
        weight_decay=0.001,
        lrf=0.001,
    )

    return results


# ----------------------------
# Plot mAP curve
# ----------------------------
def plot_map_curve(results_csv: Path):
    if not results_csv.exists():
        print("❌ results.csv not found")
        return

    df = pd.read_csv(results_csv)

    if "metrics/mAP50-95(B)" not in df.columns:
        print("❌ mAP column not found")
        return

    best_idx = df["metrics/mAP50-95(B)"].idxmax()
    best_epoch = best_idx + 1
    best_map = df["metrics/mAP50-95(B)"].max()

    plt.figure(figsize=(8, 5))
    plt.plot(df["metrics/mAP50-95(B)"], label="mAP50-95")
    plt.scatter(best_idx, best_map, label=f"Best Epoch {best_epoch}")
    plt.title("mAP50-95 vs Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("mAP50-95")
    plt.grid()
    plt.legend()
    plt.tight_layout()

    plt.savefig(results_csv.parent / "map_curve.png", dpi=200)
    plt.show()

    print(f"\n📌 Best epoch in this run: {best_epoch}")
    print(f"📌 Best mAP50-95: {best_map:.4f}")


# ----------------------------
# Save overall summary
# ----------------------------
def save_summary_from_val(val_res, save_dir: Path):
    box = getattr(val_res, "box", None)
    if box is None:
        print("❌ No validation box metrics found")
        return

    map_5095 = getattr(box, "map", None)
    map_50 = getattr(box, "map50", None)
    mp = getattr(box, "mp", None)
    mr = getattr(box, "mr", None)

    summary = {
        "run_name": RUN_NAME,
        "model": MODEL,
        "epochs": EPOCHS,
        "imgsz": IMGSZ,
        "batch": BATCH,
        "mAP": float(map_5095) if map_5095 is not None else None,
        "AP_IoU": float(map_50) if map_50 is not None else None,
        "J": float(mp) if mp is not None else None,
        "F": float(mr) if mr is not None else None,
    }

    if summary["J"] is not None and summary["F"] is not None and (summary["J"] + summary["F"]) > 0:
        summary["J&R"] = 2 * summary["J"] * summary["F"] / (summary["J"] + summary["F"])
    else:
        summary["J&R"] = None

    summary_df = pd.DataFrame([summary])
    summary_path = save_dir / "summary.csv"
    summary_df.to_csv(summary_path, index=False)

    print(f"\n💾 Summary saved to: {summary_path}")
    print(summary_df.to_string(index=False))

# ----------------------------
# Save per-class report
# ----------------------------
def save_per_class_report_from_val(val_res, save_dir: Path):
    box = getattr(val_res, "box", None)
    names = getattr(val_res, "names", {})

    if box is None:
        print("❌ No validation box metrics found")
        return

    maps = getattr(box, "maps", None)
    ap50s = getattr(box, "ap50", None)
    p = getattr(box, "p", None)
    r = getattr(box, "r", None)

    rows = []

    if maps is not None:
        num_classes = len(names)
        for cid in range(num_classes):
            cname = names[cid] if isinstance(names, dict) else str(cid)

            precision = float(p[cid]) if (p is not None and cid < len(p)) else None
            recall = float(r[cid]) if (r is not None and cid < len(r)) else None
            jr = (
                2 * precision * recall / (precision + recall)
                if (precision is not None and recall is not None and (precision + recall) > 0)
                else None
            )

            rows.append({
                "class_id": cid,
                "class_name": cname,
                "mAP": float(maps[cid]) if cid < len(maps) else None,
                "AP_IoU": float(ap50s[cid]) if (ap50s is not None and cid < len(ap50s)) else None,
                "J": precision,
                "F": recall,
                "J&R": jr,
            })

    mp = getattr(box, "mp", None)
    mr = getattr(box, "mr", None)

    overall_precision = float(mp) if mp is not None else None
    overall_recall = float(mr) if mr is not None else None
    overall_jr = (
        2 * overall_precision * overall_recall / (overall_precision + overall_recall)
        if (
            overall_precision is not None
            and overall_recall is not None
            and (overall_precision + overall_recall) > 0
        )
        else None
    )

    rows.append({
        "class_id": -1,
        "class_name": "OVERALL",
        "mAP": float(box.map) if getattr(box, "map", None) is not None else None,
        "AP_IoU": float(box.map50) if getattr(box, "map50", None) is not None else None,
        "J": overall_precision,
        "F": overall_recall,
        "J&R": overall_jr,
    })

    df = pd.DataFrame(rows)
    csv_path = save_dir / "per_class_metrics.csv"
    txt_path = save_dir / "per_class_metrics.txt"

    df.to_csv(csv_path, index=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(df.to_string(index=False))

    print(f"\n💾 Per-class CSV saved to: {csv_path}")
    print(f"💾 Per-class TXT saved to: {txt_path}")
    print(df.to_string(index=False))

# ----------------------------
# MAIN
# ----------------------------
def main():
    train_res = train_model()

    save_dir = Path(train_res.save_dir)
    print(f"\n📁 Run directory: {save_dir}")

    results_csv = save_dir / "results.csv"

    # 1) training curve
    plot_map_curve(results_csv)

    # 2) locate best.pt
    best_pt = save_dir / "weights" / "best.pt"
    last_pt = save_dir / "weights" / "last.pt"

    if best_pt.exists():
        weights_path = best_pt
        print(f"\n✅ Using best.pt: {weights_path}")
    elif last_pt.exists():
        weights_path = last_pt
        print(f"\n⚠️ best.pt not found, using last.pt: {weights_path}")
    else:
        print("\n❌ No weights found")
        return

    # 3) run validation once
    model = YOLO(str(weights_path))
    val_res = model.val(
        data=DATA_YAML,
        imgsz=IMGSZ,
        device=DEVICE,
        plots=True,
        save_json=True,
    )

    # 4) overall summary from best.pt validation
    save_summary_from_val(val_res, save_dir)

    # 5) per-class report
    save_per_class_report_from_val(val_res, save_dir)


if __name__ == "__main__":
    main()