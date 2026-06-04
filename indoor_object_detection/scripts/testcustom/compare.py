import time
import pandas as pd
import matplotlib.pyplot as plt
from ultralytics import YOLO
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------
DATA_YAML = "dataset/merge_dataset_final/data.yaml"
IMG_SIZE = 640
DEVICE = 0

CUSTOM_MODEL = "runs/detect/runs/testcustom/result_custom_45/weights/best.pt"
PRETRAINED_MODEL = "runs/detect/runs/testcustom/result_pretrained_new/weights/best.pt"

TEST_DIR = "dataset/merge_dataset_final/test/images"
OUTPUT_DIR = Path("runs/detect/runs/compareresult")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Accuracy Evaluation
# ----------------------------
def evaluate_accuracy(model_path):
    model = YOLO(model_path)

    # Validation (for training performance)
    val_res = model.val(
        data=DATA_YAML,
        imgsz=IMG_SIZE,
        device=DEVICE,
        split="val",
        verbose=False
    )

    # Test (for final evaluation)
    test_res = model.val(
        data=DATA_YAML,
        imgsz=IMG_SIZE,
        device=DEVICE,
        split="test",
        verbose=False
    )

    val_box = val_res.box
    test_box = test_res.box

    return {
        # Validation metrics
        "Val mAP@0.5": float(val_box.map50),
        "Val mAP@0.5:0.95": float(val_box.map),
        "Val Precision": float(val_box.mp),
        "Val Recall": float(val_box.mr),

        # Test metrics (MOST IMPORTANT)
        "Test mAP@0.5": float(test_box.map50),
        "Test mAP@0.5:0.95": float(test_box.map),
        "Test Precision": float(test_box.mp),
        "Test Recall": float(test_box.mr),
    }

# ----------------------------
# Speed Evaluation
# ----------------------------
def evaluate_speed(model_path, num_images=None):
    model = YOLO(model_path)
    image_paths = list(Path(TEST_DIR).glob("*.jpg"))
    
    if num_images:
        image_paths = image_paths[:min(num_images, len(image_paths))]
    
    # Better warm-up with different images
    for i in range(min(5, len(image_paths))):
        model.predict(source=str(image_paths[i]), imgsz=IMG_SIZE, device=DEVICE, verbose=False)
    
    # Measure only inference time (exclude initial load)
    start = time.time()
    for img in image_paths:
        model.predict(source=str(img), imgsz=IMG_SIZE, device=DEVICE, verbose=False)
    total_time = time.time() - start
    
    return {
        "FPS": len(image_paths) / total_time,
        "Time/Image (ms)": (total_time / len(image_paths)) * 1000,
        "NumTestImages": len(image_paths)  # Add this for transparency
    }

# ----------------------------
# Lightweight Evaluation
# ----------------------------
def evaluate_lightweight(model_path):
    model = YOLO(model_path)
    size_mb = Path(model_path).stat().st_size / (1024 * 1024)

    gflops = None
    try:
        info = model.info(verbose=True, imgsz=IMG_SIZE)
        if isinstance(info, tuple) and len(info) >= 4:
            gflops = float(info[3])
    except Exception as e:
        print(f"[WARNING] Could not compute GFLOPs: {e}")

    return {
        "Model Size (MB)": size_mb,
        "GFLOPs": gflops
    }

# ----------------------------
# Combined Evaluation
# ----------------------------
def evaluate_model(name, model_path):
    print(f"\n🔍 Evaluating {name}...")

    acc = evaluate_accuracy(model_path)

    # ----------------------------
    # Validation J&R
    # ----------------------------
    if acc["Val Precision"] + acc["Val Recall"] > 0:
        acc["Val J&R"] = 2 * acc["Val Precision"] * acc["Val Recall"] / (
            acc["Val Precision"] + acc["Val Recall"]
        )
    else:
        acc["Val J&R"] = 0

    # ----------------------------
    # Test J&R
    # ----------------------------
    if acc["Test Precision"] + acc["Test Recall"] > 0:
        acc["Test J&R"] = 2 * acc["Test Precision"] * acc["Test Recall"] / (
            acc["Test Precision"] + acc["Test Recall"]
        )
    else:
        acc["Test J&R"] = 0

    speed = evaluate_speed(model_path)
    light = evaluate_lightweight(model_path)

    return {
        "Model": name,
        **acc,
        **speed,
        **light
    }

# ----------------------------
# MAIN COMPARISON
# ----------------------------
def main():
    custom = evaluate_model("Custom", CUSTOM_MODEL)
    pretrained = evaluate_model("Pretrained", PRETRAINED_MODEL)

    df = pd.DataFrame([custom, pretrained])
    df = df.sort_values(by="Test mAP@0.5:0.95", ascending=False)

    print("\n📊 FINAL COMPARISON:")
    print(df.to_string(index=False))

    df.to_csv(OUTPUT_DIR / "final_model_comparison.csv", index=False)
    print("\n💾 Saved to final_model_comparison.csv")

    import matplotlib.pyplot as plt

    # ============================
    # 1. Accuracy Chart
    # ============================
    accuracy_metrics = [
        "Val mAP@0.5",
        "Val mAP@0.5:0.95",
        "Val Precision",
        "Val Recall",
        "Val J&R",
        "Test mAP@0.5",
        "Test mAP@0.5:0.95",
        "Test Precision",
        "Test Recall",
        "Test J&R"
    ]

    acc_df = df[["Model"] + accuracy_metrics].set_index("Model").T

    ax = acc_df.plot(kind="bar", figsize=(14, 7))

    plt.title("Accuracy Comparison Between Custom and Pretrained Models")
    plt.xlabel("Metrics")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Model")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.4f", padding=2, fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "accuracy_comparison_chart.png", dpi=300)
    plt.show()

    # ============================
    # 2. Efficiency Chart
    # ============================
    efficiency_metrics = [
        "FPS",
        "Time/Image (ms)",
        "Model Size (MB)",
        "GFLOPs"
    ]

    eff_df = df[["Model"] + efficiency_metrics].set_index("Model").T

    ax2 = eff_df.plot(kind="bar", figsize=(10, 6))

    plt.title("Efficiency Comparison Between Models")
    plt.xlabel("Metrics")
    plt.ylabel("Value")
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Model")

    for container in ax2.containers:
        ax2.bar_label(container, fmt="%.4f", padding=2, fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "efficiency_comparison_chart.png", dpi=300)
    plt.show()

    # ============================
    # 3. Validation + GFLOPs Chart
    # ============================
    selected_metrics = [
        "Val Precision",
        "Val Recall",
        "Val mAP@0.5",
        "Val mAP@0.5:0.95",
        "GFLOPs"
    ]

    extra_df = df[["Model"] + selected_metrics].set_index("Model").T

    ax3 = extra_df.plot(kind="bar", figsize=(12, 7))

    plt.title("Validation Performance and GFLOPs Comparison")
    plt.xlabel("Metrics")
    plt.ylabel("Value")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Model")

    # Add labels
    for container in ax3.containers:
        ax3.bar_label(container, fmt="%.4f", padding=2, fontsize=8)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "validation_gflops_comparison.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    main()