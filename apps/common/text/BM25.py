import math
from collections import Counter
from typing import List, Union
import jieba
from functools import lru_cache


@lru_cache(maxsize=None)
def load_stopwords(file_path='stopwords.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().strip().split('\n'))
    return stopwords


def split_doc(doc: str) -> List[str]:
    return list(jieba.cut(doc))


class BM25:
    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.stopwords = load_stopwords()
        self.corpus = [self._remove_stopwords(split_doc(doc)) for doc in corpus]
        self.k1 = k1
        self.b = b
        self.document_lengths = [len(doc) for doc in corpus]
        self.avg_doc_length = sum(self.document_lengths) / len(corpus)
        self.corpus_size = len(corpus)
        self.df = {}
        self.idf = {}
        self._initialize()

    def _initialize(self):
        """Calculate DF (document frequency) and IDF for each term in the corpus."""
        df = {}
        for document in self.corpus:
            # Use set to count each term only once per document
            for term in set(document):
                df[term] = df.get(term, 0) + 1
        self.df = df
        # Calculate IDF using the formula
        self.idf = {term: math.log((self.corpus_size - df + 0.5) / (df + 0.5)) for term, df in self.df.items()}

    def _remove_stopwords(self, document: List[str]):
        return [word for word in document if word not in self.stopwords]

    def _score(self, document: List[str], query: List[str]):
        """Calculate the BM25 score for a single document given a query."""
        score = 0.0
        doc_length = len(document)
        doc_counter = Counter(document)
        for term in query:
            if term in doc_counter:
                term_frequency = doc_counter[term]
                numerator = self.idf.get(term, 0) * (term_frequency * (self.k1 + 1))
                denominator = term_frequency + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)
                score += (numerator / denominator)
        return score

    def get_score_docs(self, query: Union[str, List[str]]):
        """Calculate scores and docs ordered by scores for all documents in the corpus."""
        """query should cut by jieba"""
        if isinstance(query, str):
            query = jieba.cut(query)
        query = self._remove_stopwords(query)
        scores = [{"score": self._score(doc, query), "doc": doc}
                  for doc in self.corpus]
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores
