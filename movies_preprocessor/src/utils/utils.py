import json
import os
import pickle


def load_pickle(path_dir: str, filename: str):
    with open(os.path.join(path_dir, filename + ".pickle"), "br") as f:
        return pickle.load(f)


def load_json(path_dir: str, filename: str):
    with open(os.path.join(path_dir, filename + ".json"), "r") as f:
        return json.load(f)
