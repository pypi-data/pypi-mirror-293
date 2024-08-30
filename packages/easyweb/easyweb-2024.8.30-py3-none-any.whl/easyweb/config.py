import os
import pathlib


class Config:
    HOME = str(pathlib.Path.home())
    EXECUTABLE_PATH = f"{HOME}/.config/browser"
    USER_DATE_DIR = "/usr/bin/browser"
    HEADLESS = True if os.environ.get("HEADLESS") is None else False


config = Config()
