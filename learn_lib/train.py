from pathlib import Path

from ultralytics import YOLO


def train_yolo(
    config_path: Path,
    epochs: int = 50,
    batch_size: int = 16,
) -> YOLO:
    """
    Train YOLO model

    Args:
        config_path (Path): Path to the config file
        epochs (int, optional): Number of epochs. Defaults to 50.
        batch_size (int, optional): Batch size. Defaults to 16.

    Returns:
        YOLO: Trained model
    """
    model = YOLO("yolov8n.pt")

    model.train(
        data=str(config_path),
        epochs=epochs,
        batch=batch_size,
    )

    return model
