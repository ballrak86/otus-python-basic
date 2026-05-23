import sys
from pathlib import Path


def add_homework_path(file):
    current_file = Path(file).resolve()
    print(f"current_file = {current_file}")
    folder_test_homework_0X = current_file.parent
    print(f"folder_test_homework_0X = {folder_test_homework_0X}")
    homework_0X = folder_test_homework_0X.name.replace("test_", "")
    print(f"homework_0X = {homework_0X}")
    homework_0X_path = folder_test_homework_0X.parent.parent / homework_0X
    print(f"homework_0X_path = {homework_0X_path}")

    sys.path.insert(0, str(homework_0X_path))
    print("Added homework package to path:", homework_0X_path)


add_homework_path(__file__)
