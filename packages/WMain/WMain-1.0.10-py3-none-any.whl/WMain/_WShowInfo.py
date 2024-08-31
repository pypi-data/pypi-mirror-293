import os


def get_line_num(file_path: str, types: list) -> int:
    line_num = 0
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file = os.path.join(root, file)
            if (
                os.path.isdir(file)
                or file.find(".") == -1
                or file.split(".")[-1] not in types
            ):
                continue
            f = open(file, "r", encoding="utf-8")
            for line in f:
                line = line.strip()
                if line:
                    line_num += 1
            f.close()
    return line_num


if __name__ == "__main__":
    char_num = 0
    line_num = get_line_num("D:/EasyCode", ["cpp", "py", "c"])
    print(f"Total line number: {line_num}")
