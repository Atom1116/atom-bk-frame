import os


def create_dir(path: str) -> None:
    """フォルダを作成。既に存在している場合、作成しない。"""
    if not os.path.isdir(path):
        os.makedirs(path)
