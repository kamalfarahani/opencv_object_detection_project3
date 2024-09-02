import random

import numpy as np
import cv2
import matplotlib.pyplot as plt


from pathlib import Path
from ultralytics import YOLO


def infer_random_images(
    model: YOLO,
    images_dir: Path,
    number_of_images=3,
) -> None:
    """
    Runs inference on random images and shows the results

    Args:
        images_dir (Path): Path to the images directory
        number_of_images (int, optional): Number of images to predict. Defaults to 3.

    Returns:
        None
    """
    random_images = random.sample(
        list(images_dir.glob("*.jpg")),
        number_of_images,
    )

    images = []
    for img_path in random_images:
        img = cv2.imread(str(img_path))
        results = model.predict(source=img_path)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        images.append(img)

    for img in images:
        plt.imshow(img)
        plt.show()
