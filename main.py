from pathlib import Path

from learn_lib.train import train_yolo
from learn_lib.validate import validate_yolo


def main() -> None:
    model = train_yolo(config_path=Path("./config.yml"))
    validate_yolo(model=model)


if __name__ == "__main__":
    main()
