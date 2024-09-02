import random

import cv2
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path


type Rect = tuple[int, int, int, int]


def read_labels(label_path: Path) -> list[Rect]:
    """
    Changes the format from (x_center, y_center, width, height) to (x_min, y_min, x_max, y_max)

    Args:
        label_path (Path): Path to the label file

    Returns:
        list[Rect]: List of rects
    """
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
    """
    Shows the image and the labels

    Args:
        img_path (Path): Path to the image
        label_path (Path): Path to the label file

    Returns:
        None
    """
    img = cv2.imread(str(img_path))
    img_width, img_height = img.shape[1], img.shape[0]
    labels = read_labels(label_path)
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


def show_random_images(
    images_dir: Path,
    labels_dir: Path,
    number_of_images: int = 5,
) -> None:
    """
    Shows random images and their labels

    Args:
        images_dir (Path): Path to the images directory
        labels_dir (Path): Path to the labels directory
        number_of_images (int, optional): Number of images to show. Defaults to 5.

    Returns:
        None
    """
    random_images = random.sample(
        list(images_dir.glob("*.jpg")),
        number_of_images,
    )
    for img_path in random_images:
        label_path = labels_dir / f"{img_path.stem}.txt"
        show_img(img_path, label_path)
