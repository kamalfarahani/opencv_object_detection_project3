import cv2
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path


type Rect = tuple[int, int, int, int]


def read_labels(label_path: Path) -> list[Rect]:
    labels = []
    with open(label_path) as f:
        for line in f:
            splited = line.split(" ")
            x_center, y_center, width, height = splited[1:]
            labels.append(
                (
                    float(x_center),
                    float(y_center),
                    float(width),
                    float(height),
                ),
            )

    # Change the format from (x_center, y_center, width, height) to (x_min, y_min, x_max, y_max)
    return [(x1 - w / 2, y1 - h / 2, x1 + w / 2, y1 + h / 2) for x1, y1, w, h in labels]


def show_img(img_path: Path, label_path: Path) -> None:
    img = cv2.imread(str(img_path))
    img_width, img_height = img.shape[1], img.shape[0]
    labels = read_labels(label_path)
    print(f"{img_path}: {labels}")
    for x1, y1, x2, y2 in labels:
        x1, y1, x2, y2 = (
            int(x1 * img_width),
            int(y1 * img_height),
            int(x2 * img_width),
            int(y2 * img_height),
        )

        if x2 > img.shape[1] or y2 > img.shape[0]:
            print(f"{img_path}: img is out of bound!")
            continue

        cv2.rectangle(
            img,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2,
        )

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


if __name__ == "__main__":
    images_path = Path(input("Enter images path: "))
    labels_path = Path(input("Enter labels path: "))

    for img_path in images_path.glob("*.jpg"):
        label_path = labels_path / f"{img_path.stem}.txt"
        show_img(img_path, label_path)
