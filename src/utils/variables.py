import os
from pathlib import Path

ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
DATA_PATH = ROOT_PATH / "data"
SRC_PATH = ROOT_PATH / "src"
MODEL_PATH = DATA_PATH / "model"
