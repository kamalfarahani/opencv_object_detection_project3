import cv2

from pathlib import Path


def normalize_bounding_boxes(images_path: Path, labels_path: Path) -> None:
    for img_path in images_path.glob("*.jpg"):
        print(img_path)
        img = cv2.imread(str(img_path))
        img_width, img_height = img.shape[1], img.shape[0]
        label_path = labels_path / f"{img_path.stem}.txt"

        normalized_lines = []
        with open(label_path) as f:
            for line in f:
                splited = line.split(" ")
                cls, x_center, y_center, width, height = splited
                x_center, y_center, width, height = (
                    float(x_center),
                    float(y_center),
                    float(width),
                    float(height),
                )

                x_center_norm = x_center / img_width
                y_center_norm = y_center / img_height
                width_norm = width / img_width
                height_norm = height / img_height

                normalized_lines.append(
                    f"{cls} {x_center_norm} {y_center_norm} {width_norm} {height_norm}"
                )

        with open(label_path, "w") as f:
            f.write("\n".join(normalized_lines))

    print("Done!")


def main() -> None:
    images_path = Path(input("Enter images path: "))
    labels_path = Path(input("Enter labels path: "))

    normalize_bounding_boxes(images_path, labels_path)


if __name__ == "__main__":
    main()
