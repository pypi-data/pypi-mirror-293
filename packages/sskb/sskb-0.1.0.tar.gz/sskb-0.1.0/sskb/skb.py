import os
import gdown
from pathlib import Path
from typing import Sequence
from .data_model import Statement, Entity

BASE_PATH = ".sskb_data"
BASE_URL = "http://personalpages.manchester.ac.uk/staff/danilo.carvalho/sskb/"


class KnowledgeBase(Sequence[Statement]):
    def __init__(self, path: str, url: str, **kwargs):
        self.data_path: str = os.path.normpath(os.path.join(str(Path.home()), BASE_PATH, path))
        if (not os.path.exists(self.data_path) and url):
            os.makedirs(os.path.join(*os.path.split(self.data_path)[:-1]), exist_ok=True)
            gdown.download(url, self.data_path)
        self.id = ""
        self.entities: list[Entity] = list()

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, index):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError



