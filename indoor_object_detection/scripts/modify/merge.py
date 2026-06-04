import os
import shutil
import yaml

SOURCE_ROOT = "dataset/final_dataset"
TARGET_ROOT = "dataset/merge_dataset_final"

SPLITS = ["train", "valid", "test"]
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp")

# ---------------- CLEAN TARGET ---------------- #

if os.path.exists(TARGET_ROOT):
    shutil.rmtree(TARGET_ROOT)

for split in SPLITS:
    os.makedirs(os.path.join(TARGET_ROOT, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_ROOT, split, "labels"), exist_ok=True)

# ---------------- CLASS MAPPING ---------------- #

class_names = sorted([
    d for d in os.listdir(SOURCE_ROOT)
    if os.path.isdir(os.path.join(SOURCE_ROOT, d))
])

class_to_id = {name: idx for idx, name in enumerate(class_names)}

print("📌 Class mapping:")
for k, v in class_to_id.items():
    print(f"  {v}: {k}")

# ---------------- LABEL CHECKING FUNCTION ---------------- #

def validate_and_remap_label_lines(lines, new_class_id, src_lbl_path):
    """
    Validates YOLO labels and converts Polygons to Bounding Boxes.
    Returns: (is_valid, cleaned_lines, error_info_list)
    """
    cleaned_lines = []
    removed_info = []
    
    for line_no, line in enumerate(lines, start=1):
        line_content = line.strip()
        if not line_content:
            continue
            
        parts = line_content.split()
        
        try:
            # Case 1: Polygon (more than 5 parts)
            if len(parts) > 5:
                coords = list(map(float, parts[1:]))
                xs = coords[0::2]
                ys = coords[1::2]
                
                xmin, xmax = min(xs), max(xs)
                ymin, ymax = min(ys), max(ys)
                
                xc = (xmin + xmax) / 2
                yc = (ymin + ymax) / 2
                w = xmax - xmin
                h = ymax - ymin
            
            # Case 2: Standard Bounding Box (5 parts)
            elif len(parts) == 5:
                _, xc, yc, w, h = map(float, parts)
            
            # Case 3: Invalid format
            else:
                removed_info.append((src_lbl_path, line_no, f"Invalid format ({len(parts)} values)", line_content))
                continue

            # Check if coordinates are normalized (0.0 to 1.0)
            if 0 <= xc <= 1 and 0 <= yc <= 1 and 0 < w <= 1 and 0 < h <= 1:
                cleaned_lines.append(f"{new_class_id} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")
            else:
                removed_info.append((src_lbl_path, line_no, f"Out of bounds (xc:{xc:.2f}, w:{w:.2f})", line_content))

        except Exception as e:
            removed_info.append((src_lbl_path, line_no, f"Error: {str(e)}", line_content))

    # File is valid only if it contains at least one valid label
    if cleaned_lines:
        return True, cleaned_lines, []
    else:
        # If no valid lines were found, return the errors gathered
        if not removed_info:
            removed_info.append((src_lbl_path, 0, "File is empty after cleaning", ""))
        return False, [], removed_info

# ---------------- MERGE ---------------- #

copied_images = 0
written_labels = 0
skipped_missing_label = 0
skipped_invalid_label = 0
removed_examples = []

for class_name, class_id in class_to_id.items():
    class_dir = os.path.join(SOURCE_ROOT, class_name)

    for split in SPLITS:
        img_src = os.path.join(class_dir, split, "images")
        lbl_src = os.path.join(class_dir, split, "labels")

        if not os.path.exists(img_src):
            continue

        for img_file in os.listdir(img_src):
            if not img_file.lower().endswith(IMAGE_EXTS):
                continue

            base = os.path.splitext(img_file)[0]

            src_img = os.path.join(img_src, img_file)
            src_lbl = os.path.join(lbl_src, base + ".txt")

            dst_img = os.path.join(TARGET_ROOT, split, "images", img_file)
            dst_lbl = os.path.join(TARGET_ROOT, split, "labels", base + ".txt")

            # skip if label file missing
            if not os.path.exists(src_lbl):
                skipped_missing_label += 1
                removed_examples.append((src_lbl, 0, "missing label file", ""))
                continue

            with open(src_lbl, "r", encoding="utf-8") as f:
                lines = f.readlines()

            is_valid_file, new_lines, removed_info = validate_and_remap_label_lines(
                lines, class_id, src_lbl
            )

            if not is_valid_file:
                skipped_invalid_label += 1
                removed_examples.extend(removed_info[:5])
                continue

            # only copy if label file is fully valid
            shutil.copy2(src_img, dst_img)
            copied_images += 1

            with open(dst_lbl, "w", encoding="utf-8") as f:
                f.write("\n".join(new_lines))
            written_labels += 1

print("\n✅ Merge complete")
print(f"🖼️ Images copied: {copied_images}")
print(f"📝 Label files written: {written_labels}")
print(f"⚠️ Skipped images with missing label file: {skipped_missing_label}")
print(f"❌ Skipped image+label pairs with invalid labels: {skipped_invalid_label}")

if removed_examples:
    print("\n🔍 Example skipped files:")
    for path, line_no, reason, line in removed_examples:
        if line_no > 0:
            print(f"{path} | line {line_no} | {reason}")
            print(f"  {line}")
        else:
            print(f"{path} | {reason}")

# ---------------- WRITE data.yaml ---------------- #

data_yaml = {
    "path": os.path.abspath(TARGET_ROOT),
    "train": "train/images",
    "val": "valid/images",
    "test": "test/images",
    "nc": len(class_names),
    "names": class_names
}

with open(os.path.join(TARGET_ROOT, "data.yaml"), "w", encoding="utf-8") as f:
    yaml.dump(data_yaml, f, sort_keys=False, allow_unicode=True)

print("\n🧾 data.yaml generated")
print("🎉 YOLO multi-class dataset is READY")