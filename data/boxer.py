from pathlib import Path


def to_yolo_box(file_path: Path) -> str:
    result_lines = []
    with open(file_path) as f:
        for line in f:
            if line.startswith("Vehicle registration plate"):
                splited = line.split(" ")
                x_min, y_min, x_max, y_max = splited[3:]

                width = float(x_max) - float(x_min)
                height = float(y_max) - float(y_min)

                x_center = float(x_min) + width / 2
                y_center = float(y_min) + height / 2

                result_lines.append(f"0 {x_center} {y_center} {width} {height}")

    return "\n".join(result_lines)


def convert_labels_to_yolo(dir_path: Path) -> None:
    for file_path in dir_path.glob("*.txt"):
        new_content = to_yolo_box(file_path)
        with open(file_path, "w") as f:
            f.write(new_content)


if __name__ == "__main__":
    path = input("Enter path: ")
    convert_labels_to_yolo(Path(path))
    print("Done!")
