import os
import yaml
import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# =========================
# CONFIG
# =========================
DATASET_PATH = "dataset/merge_dataset_raw"
YAML_PATH = os.path.join(DATASET_PATH, "data.yaml")

TRAIN_LABEL_DIR = os.path.join(DATASET_PATH, "train", "labels")
IMAGE_DIR = os.path.join(DATASET_PATH, "train", "images")

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp")


# =========================
# EDA FUNCTIONS
# =========================
def load_eda_data():
    """
    Train-only EDA:
    - load class names from data.yaml
    - count class instances from train labels only
    - collect bbox width, height, area
    """
    if not os.path.exists(YAML_PATH):
        raise FileNotFoundError(f"Dataset YAML not found: {YAML_PATH}")

    with open(YAML_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    class_names = data["names"]
    if isinstance(class_names, dict):
        class_names = [class_names[i] for i in range(len(class_names))]

    class_counts = Counter()
    image_counts = Counter()
    widths, heights, areas = [], [], []

    total_images_with_labels = 0
    empty_labels = 0

    if not os.path.exists(TRAIN_LABEL_DIR):
        raise FileNotFoundError(f"Train label directory not found: {TRAIN_LABEL_DIR}")

    for file in os.listdir(TRAIN_LABEL_DIR):
        if not file.endswith(".txt"):
            continue

        file_path = os.path.join(TRAIN_LABEL_DIR, file)

        classes_in_this_image = []
        has_valid_label = False

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) != 5:
                    continue

                class_id = int(float(parts[0]))
                _, _, _, w, h = map(float, parts)

                class_counts[class_id] += 1
                widths.append(w)
                heights.append(h)
                areas.append(w * h)

                classes_in_this_image.append(class_id)
                has_valid_label = True

        if has_valid_label:
            total_images_with_labels += 1
            for cls_id in set(classes_in_this_image):
                image_counts[cls_id] += 1
        else:
            empty_labels += 1

    return class_names, class_counts, image_counts, widths, heights, areas, total_images_with_labels, empty_labels


def classify_bbox_sizes(areas):
    size_counts = {"Small (<2%)": 0, "Medium (2-10%)": 0, "Large (>10%)": 0}

    for area in areas:
        if area < 0.02:
            size_counts["Small (<2%)"] += 1
        elif area < 0.10:
            size_counts["Medium (2-10%)"] += 1
        else:
            size_counts["Large (>10%)"] += 1

    return size_counts


def print_class_distribution(class_names, class_counts, image_counts):
    print(f"{'Class':<10}{'Instances':<15}{'Images':<10}")
    print("-" * 60)

    for cls_id in range(len(class_names)):
        print(
            f"{cls_id:<10}"
            f"{class_counts.get(cls_id, 0):<15}"
            f"{image_counts.get(cls_id, 0):<10}"
        )


def print_bbox_statistics(class_names, class_counts, widths, heights, areas, total_images_with_labels, empty_labels):
    total_objects = len(areas)
    avg_width = np.mean(widths) if widths else 0
    avg_height = np.mean(heights) if heights else 0
    avg_area = np.mean(areas) if areas else 0

    print("\n📦 TRAIN BOUNDING BOX STATISTICS")
    print("-" * 60)
    print(f"Total train images with labels : {total_images_with_labels:,}")
    print(f"Empty labels                   : {empty_labels:,}")
    print(f"Total object instances         : {total_objects:,}")
    print(f"Number of classes              : {len(class_names)}")
    print(f"Average bbox width             : {avg_width:.4f}")
    print(f"Average bbox height            : {avg_height:.4f}")
    print(f"Average bbox area              : {avg_area:.4f}")

    if class_counts:
        max_class = max(class_counts, key=class_counts.get)
        print(f"Most common class              : {class_names[max_class]} ({class_counts[max_class]})")


def print_size_distribution(size_counts, total_objects):
    print("\n📏 BOUNDING BOX SIZE DISTRIBUTION (TRAIN ONLY)")
    print("-" * 60)
    for size_name, count in size_counts.items():
        pct = (count / total_objects * 100) if total_objects > 0 else 0
        print(f"{size_name:<20}: {count:<8} ({pct:.2f}%)")


def print_key_insights(class_names, class_counts, size_counts, areas):
    total_objects = len(areas)
    small_objects_pct = (
        size_counts["Small (<2%)"] / total_objects * 100
        if total_objects > 0
        else 0
    )

    print("\n📌 KEY INSIGHTS")
    print("-" * 60)
    print(f"Total objects analyzed      : {total_objects:,}")
    print(f"Number of classes           : {len(class_names)}")
    print("Dataset analyzed across     : Train split only")
    print(f"Small objects presence      : {small_objects_pct:.1f}% of all objects are small (<2% area)")

    print("\n💡 RECOMMENDATIONS")
    print("-" * 60)
    if small_objects_pct > 30:
        print("- Consider using higher input resolution (e.g. 1280px)")
        print("- Consider mosaic/mixup augmentation for small objects")
        print("- Consider re-clustering anchor boxes for small objects")
    else:
        print("- Dataset appears acceptable in terms of object size distribution")
        print("- Current configuration should work reasonably well for most objects")


def save_class_distribution_plot(class_names, class_counts, output_path):
    sorted_items = sorted(class_counts.items(), key=lambda x: x[1], reverse=True)

    if not sorted_items:
        print("⚠️ No class counts available for plotting.")
        return

    classes, counts = zip(*sorted_items)
    labels = [class_names[i] for i in classes]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(labels, counts, color="skyblue", edgecolor="navy")
    ax.set_xlabel("Class Name", fontsize=10)
    ax.set_ylabel("Number of Objects", fontsize=10)
    ax.set_title("Class Distribution Across Training Dataset", fontsize=12, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"✅ Saved class distribution plot: {output_path}")


def save_size_distribution_plot(size_counts, output_path):
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#ff9999", "#66b3ff", "#99ff99"]
    bars = ax.bar(size_counts.keys(), size_counts.values(), color=colors, edgecolor="black")
    ax.set_xlabel("Object Size Category", fontsize=10)
    ax.set_ylabel("Number of Objects", fontsize=10)
    ax.set_title("Object Size Distribution (Train Split)", fontsize=12, fontweight="bold")

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.xticks(rotation=0, fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"✅ Saved size distribution plot: {output_path}")


def save_sample_annotated_image(class_names, output_path, selected_img=None):
    if not os.path.exists(IMAGE_DIR):
        print(f"⚠️ Image directory not found: {IMAGE_DIR}")
        return

    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(IMAGE_EXTS)]
    if not image_files:
        print("⚠️ No images found in the dataset.")
        return

    image_files.sort()

    if selected_img is None:
        selected_img = image_files[0]

    if selected_img not in image_files:
        print(f"⚠️ Selected image not found: {selected_img}")
        return

    img_path = os.path.join(IMAGE_DIR, selected_img)
    base = os.path.splitext(selected_img)[0]
    label_path = os.path.join(DATASET_PATH, "train", "labels", base + ".txt")

    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ Could not load image: {img_path}")
        return

    h, w = img.shape[:2]

    if os.path.exists(label_path):
        with open(label_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) != 5:
                    continue

                cls, x, y, bw, bh = map(float, parts)
                cls = int(cls)

                x1 = int((x - bw / 2) * w)
                y1 = int((y - bh / 2) * h)
                x2 = int((x + bw / 2) * w)
                y2 = int((y + bh / 2) * h)

                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = class_names[cls] if cls < len(class_names) else str(cls)
                cv2.putText(
                    img,
                    label,
                    (x1, max(20, y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

    ok = cv2.imwrite(output_path, img)
    if ok:
        print(f"✅ Saved sample annotated image: {output_path}")
        print(f"   Source image: {selected_img}")
    else:
        print(f"⚠️ Failed to save annotated image: {output_path}")


# =========================
# MAIN TERMINAL RUNNER
# =========================
def main():
    print("📊 Dataset Exploratory Data Analysis (EDA)")
    print("=" * 60)

    try:
        (
            class_names,
            class_counts,
            image_counts,
            widths,
            heights,
            areas,
            total_images_with_labels,
            empty_labels,
        ) = load_eda_data()

        if not class_counts:
            print("⚠️ No valid labels found in training dataset.")
            return

        size_counts = classify_bbox_sizes(areas)

        output_dir = os.path.join(DATASET_PATH, "eda_outputs_train")
        os.makedirs(output_dir, exist_ok=True)

        # ================================
        # 1️⃣ CLASS DISTRIBUTION
        # ================================
        print("\n1️⃣ Class Distribution (Instance-based)")
        print("-" * 60)
        print_class_distribution(class_names, class_counts, image_counts)

        save_class_distribution_plot(
            class_names,
            class_counts,
            os.path.join(output_dir, "train_class_distribution.png"),
        )

        # ================================
        # 2️⃣ BOUNDING BOX SIZE DISTRIBUTION
        # ================================
        print("\n2️⃣ Bounding Box Size Distribution")
        print("-" * 60)
        print_size_distribution(size_counts, len(areas))

        save_size_distribution_plot(
            size_counts,
            os.path.join(output_dir, "train_bbox_size_distribution.png"),
        )

        # ================================
        # 3️⃣ BOUNDING BOX STATISTICS
        # ================================
        print("\n3️⃣ Bounding Box Statistics")
        print("-" * 60)
        print_bbox_statistics(
            class_names,
            class_counts,
            widths,
            heights,
            areas,
            total_images_with_labels,
            empty_labels,
        )

        # ================================
        # 4️⃣ SAMPLE ANNOTATED IMAGE
        # ================================
        print("\n4️⃣ Sample Annotated Image")
        print("-" * 60)

        save_sample_annotated_image(
            class_names,
            os.path.join(output_dir, "train_sample_annotated_image.jpg"),
        )

        # ================================
        # 5️⃣ KEY INSIGHTS
        # ================================
        print("\n5️⃣ Key Insights")
        print("-" * 60)
        print_key_insights(class_names, class_counts, size_counts, areas)

        print("\n✅ Train-only EDA completed successfully.")
        print(f"📁 Outputs saved in: {output_dir}")

    except Exception as e:
        print(f"❌ Error loading EDA data: {e}")

if __name__ == "__main__":
    main()