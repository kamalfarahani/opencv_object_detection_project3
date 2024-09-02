from pathlib import Path

from ultralytics import YOLO


def validate_yolo(model: YOLO) -> dict:
    results = model.val()

    return results
