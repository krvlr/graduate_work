import logging
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
from core.config import base_settings
from fastapi import Depends
from gensim.models.phrases import Phrases
from nltk.stem import WordNetLemmatizer
from utils.utils import load_json

logger = logging.getLogger(__name__)


phrases: Phrases | None = None


def get_phrases():
    return phrases


class IPreprocessor(ABC):
    @abstractmethod
    def process_texts(self, texts: list[str]):
        pass


class NltkPreprocessor(IPreprocessor):
    def __init__(
        self,
        phrases: Phrases,
        stopwords_filenames: list[str],
        stopwords_path: str,
    ):
        self.lemmatizer = WordNetLemmatizer()
        self.phrases: Phrases = phrases
        self.stopwords = self.load_all_stopwords(
            stopwords_path=stopwords_path, stopwords_filenames=stopwords_filenames
        )

    def load_all_stopwords(self, stopwords_path: str, stopwords_filenames: list[str]) -> set:
        all_stopwords = set()

        for filename in stopwords_filenames:
            stopwords = load_json(
                path_dir=os.path.join(Path.cwd(), stopwords_path), filename=filename
            )
            all_stopwords |= set(stopwords)
            all_stopwords |= set([self.lemmatizer.lemmatize(stopword) for stopword in stopwords])

        return all_stopwords

    def clean_text(self, text: str):
        if pd.isna(text):
            return ""
        else:
            text = text.lower()
            text = re.sub(r"<[^>]+>", "", text)
            text = re.sub(r"[_-]", " ", text)
            text = re.sub(r"[^\sa-z]", " ", text)
            lemmas = [
                self.lemmatizer.lemmatize(tok)
                for tok in text.split()
                if tok not in self.stopwords and self.lemmatizer.lemmatize(tok) not in self.stopwords
            ]
            text = " ".join(self.phrases[lemmas])
            return text

    def process_text(self, text: str) -> str:
        processed_text = self.clean_text(text)
        return processed_text

    def process_texts(self, texts: list[str]) -> list[str]:
        logger.info("Start process texts")
        processed_texts = [self.process_text(text) for text in texts]
        return processed_texts


def get_preprocessor(phrases=Depends(get_phrases)):
    preprocessor = NltkPreprocessor(
        phrases=phrases,
        stopwords_filenames=base_settings.stopwords_filenames,
        stopwords_path=base_settings.stopwords_path,
    )
    return preprocessor
