from pathlib import Path
import shutil


def list_items(folder_path):
    return list(folder_path.iterdir())


def create_file(file_path):
    with open(file_path, "x") as file:
        file.write("")


def create_folder(folder_path):
    folder_path.mkdir()


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def save_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)


def delete_item(item_path):
    if item_path.is_dir():
        if any(item_path.iterdir()):
            raise OSError("Directory is not empty")
        item_path.rmdir()
    else:
        item_path.unlink()


def rename_item(old_path, new_path):
    old_path.rename(new_path)


def get_properties(item_path):
    return item_path.stat()