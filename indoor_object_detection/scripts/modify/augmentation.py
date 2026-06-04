import os
import cv2
import random
import uuid
from collections import defaultdict
import albumentations as A

# =========================
# CONFIG
# =========================
DATA_ROOT = "dataset/merge_dataset_final"
SPLIT = "train" 
IMG_DIR = os.path.join(DATA_ROOT, SPLIT, "images")
LBL_DIR = os.path.join(DATA_ROOT, SPLIT, "labels")

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp")

# Target count per class (INSTANCE count)
TARGET_PER_CLASS = 1200

# How many tries to allow per needed sample
MAX_TRIES_MULTIPLIER = 6

random.seed(42)

# =========================
# AUGMENTATION PIPELINE
# YOLO bboxes: (class_id, x_center, y_center, w, h) normalized
# =========================
transform = A.Compose(
    [
        # ---- Geometry ----
        A.OneOf(
            [
                A.Affine(
                    translate_percent={"x": (-0.05, 0.05), "y": (-0.05, 0.05)},
                    scale=(0.90, 1.10),
                    rotate=(-12, 12),
                    shear=(-6, 6),
                    p=1.0,
                ),
                A.Perspective(scale=(0.02, 0.05), keep_size=True, p=1.0),
            ],
            p=0.4,
        ),

        # ---- Lighting / color ----
        A.RandomBrightnessContrast(p=0.6),
        A.HueSaturationValue(
            hue_shift_limit=8,
            sat_shift_limit=12,
            val_shift_limit=10,
            p=0.35,
        ),
        A.RandomGamma(gamma_limit=(85, 115), p=0.25),

        # ---- Noise / blur ----
        A.OneOf(
            [
                A.GaussNoise(p=1.0),
                A.MotionBlur(blur_limit=5, p=1.0),
                A.GaussianBlur(blur_limit=5, p=1.0),
            ],
            p=0.25,
        ),

        # ---- Occlusion robustness ----
        A.CoarseDropout(p=0.20),

        # ---- Flip ----
        A.HorizontalFlip(p=0.35),
    ],
    bbox_params=A.BboxParams(
        format="yolo",
        label_fields=["class_labels"],
        min_area=16,
        min_visibility=0.25,
        clip=True,
    ),
)

# =========================
# HELPERS
# =========================
def list_images():
    files = []

    if not os.path.isdir(IMG_DIR):
        print(f"❌ Image directory not found: {IMG_DIR}")
        return files

    if not os.path.isdir(LBL_DIR):
        print(f"❌ Label directory not found: {LBL_DIR}")
        return files

    for f in os.listdir(IMG_DIR):
        if f.lower().endswith(IMAGE_EXTS):
            base = os.path.splitext(f)[0]
            lbl_path = os.path.join(LBL_DIR, base + ".txt")
            if os.path.exists(lbl_path):
                files.append(f)

    return files


def read_yolo_label(path):
    bboxes = []
    class_labels = []

    if not os.path.exists(path):
        return bboxes, class_labels

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) != 5:
                continue

            try:
                cls = int(float(parts[0]))   # changed here
                x, y, w, h = map(float, parts[1:])
            except ValueError:
                continue

            bboxes.append([x, y, w, h])
            class_labels.append(cls)

    return bboxes, class_labels


def write_yolo_label(path, bboxes, class_labels):
    with open(path, "w") as f:
        for bb, cls in zip(bboxes, class_labels):
            x, y, w, h = bb
            cls = int(float(cls))  
            f.write(f"{cls} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")


def count_instances_per_class(image_files):
    """
    class_counts:
        total number of object instances (boxes) per class

    class_to_images:
        mapping from class -> list of images containing that class
    """
    class_to_images = defaultdict(list)
    class_counts = defaultdict(int)

    for img_file in image_files:
        base = os.path.splitext(img_file)[0]
        lbl_path = os.path.join(LBL_DIR, base + ".txt")

        _, class_labels = read_yolo_label(lbl_path)
        if not class_labels:
            continue

        # count every instance
        for c in class_labels:
            class_counts[c] += 1

        # build image pool for each class
        for c in set(class_labels):
            class_to_images[c].append(img_file)

    return class_counts, class_to_images


def unique_out_name(original_base):
    return f"{original_base}_aug_{uuid.uuid4().hex[:10]}"


# =========================
# MAIN
# =========================
def main():
    image_files = list_images()

    if not image_files:
        print("❌ No valid training images with matching label files found.")
        return

    class_counts, class_to_images = count_instances_per_class(image_files)
    all_classes = sorted(class_counts.keys())

    if not all_classes:
        print("❌ No classes found in label files.")
        return

    print("📊 Current train INSTANCE counts per class:")
    for c in all_classes:
        print(f"  class {c}: {class_counts[c]}")

    print(f"\n🎯 Target per class (instances): {TARGET_PER_CLASS}")
    print("🚀 Starting augmentation...\n")

    # Track how many augmented images were created for each class
    aug_images_made_per_class = defaultdict(int)

    # Track how many new instances were added for each class
    aug_instances_added_per_class = defaultdict(int)

    for c in all_classes:
        current = class_counts[c]

        if current >= TARGET_PER_CLASS:
            print(f"⏭️ class {c}: already at target ({current}), skipping")
            continue

        need = TARGET_PER_CLASS - current
        pool = class_to_images[c]

        if not pool:
            print(f"⚠️ class {c}: no images found, skipping")
            continue

        tries_left = max(need * MAX_TRIES_MULTIPLIER, 50)
        made_images = 0
        added_instances = 0

        while added_instances < need and tries_left > 0:
            tries_left -= 1

            img_file = random.choice(pool)
            base = os.path.splitext(img_file)[0]
            img_path = os.path.join(IMG_DIR, img_file)
            lbl_path = os.path.join(LBL_DIR, base + ".txt")

            image = cv2.imread(img_path)
            if image is None:
                continue

            bboxes, class_labels = read_yolo_label(lbl_path)
            if not bboxes:
                continue

            try:
                out = transform(image=image, bboxes=bboxes, class_labels=class_labels)
            except Exception:
                continue

            out_img = out["image"]
            out_bboxes = out["bboxes"]
            out_labels = out["class_labels"]

            if not out_bboxes or not out_labels:
                continue

            # count how many instances of target class remain after augmentation
            num_target_in_new = sum(1 for lbl in out_labels if lbl == c)

            if num_target_in_new == 0:
                continue

            # save augmented sample
            new_base = unique_out_name(base)
            new_img_path = os.path.join(IMG_DIR, new_base + ".jpg")
            new_lbl_path = os.path.join(LBL_DIR, new_base + ".txt")

            ok = cv2.imwrite(new_img_path, out_img)
            if not ok:
                continue

            write_yolo_label(new_lbl_path, out_bboxes, out_labels)

            made_images += 1
            added_instances += num_target_in_new
            aug_images_made_per_class[c] += 1
            aug_instances_added_per_class[c] += num_target_in_new

        print(
            f"✅ class {c}: generated {made_images} images, "
            f"added {added_instances} instances / needed {need} "
            f"(tries left: {tries_left})"
        )

    print("\n🎉 Augmentation done.\n")

    print("📌 Summary (extra augmented images generated per class):")
    for c in all_classes:
        if aug_images_made_per_class[c] > 0:
            print(f"  class {c}: +{aug_images_made_per_class[c]} images")

    print("\n📌 Summary (extra instances added per class):")
    for c in all_classes:
        if aug_instances_added_per_class[c] > 0:
            print(f"  class {c}: +{aug_instances_added_per_class[c]} instances")

    print("\n📌 Estimated final instance counts per class:")
    for c in all_classes:
        final_count = class_counts[c] + aug_instances_added_per_class[c]
        print(f"  class {c}: {final_count}")

    print("\n✅ TRAIN split is now more balanced by INSTANCE count.")
    print("⚠️ Validation/test were NOT changed.")


if __name__ == "__main__":
    main()