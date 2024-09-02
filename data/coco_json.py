import json

import cv2

from pathlib import Path


def to_coco_format(images_path: Path, labels_path: Path) -> dict:
    images = []
    annotations = []
    for image_path in images_path.glob("*.jpg"):
        image_id = image_path.stem
        image = cv2.imread(str(image_path))
        height, width, _ = image.shape
        images.append(
            {
                "id": image_id,
                "height": height,
                "width": width,
                "file_name": image_path.name,
            }
        )

    label_id = 1
    for label_path in labels_path.glob("*.txt"):
        image_id = label_path.stem
        # Find image with the same id
        image_info = next(image for image in images if image["id"] == image_id)
        image_width, image_height = image_info["width"], image_info["height"]

        with open(label_path) as f:
            for line in f:
                splited = line.split(" ")
                category_id = int(splited[0])
                x_center, y_center, box_width, box_height = map(float, splited[1:])
                x = x_center - box_width / 2
                y = y_center - box_height / 2

                # Convert to COCO format
                x = x * image_width
                y = y * image_height
                box_width = box_width * image_width
                box_height = box_height * image_height

                annotations.append(
                    {
                        "id": label_id,
                        "image_id": image_id,
                        "category_id": category_id,
                        "bbox": [x, y, box_width, box_height],
                        "area": box_width * box_height,
                        "iscrowd": 0,
                    }
                )

                label_id += 1

    return {
        "images": images,
        "annotations": annotations,
        "categories": [
            {
                "id": 0,
                "name": "vehicle registration plate",
            }
        ],
    }


if __name__ == "__main__":
    images_path = Path(input("Enter images path: "))
    labels_path = Path(input("Enter labels path: "))
    coco_json = to_coco_format(images_path, labels_path)

    with open("coco.json", "w") as f:
        json.dump(coco_json, f)
