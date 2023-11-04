import numpy as np


class CompareSignatures:
    @staticmethod
    def sim(s1: np.ndarray, s2: np.ndarray) -> float:
        """
        Compare the similarity of two documents based on their signatures, using Jaccard similarity.
        :param s1: Signature of document1.
        :param s2: Signature of document2.
        :return: Similarity of document1 and document2.
        """

        return np.count_nonzero(s1 == s2) / np.shape(s1)[0]
