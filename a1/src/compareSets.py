from typing import Set


class CompareSets:
    @staticmethod
    def sim(s1: Set[int], s2: Set[int]) -> float:
        """
        Compare the similarity of two documents based on their shingles, using Jaccard similarity.
        :param s1: Shingles of document1.
        :param s2: Shingles of document2.
        :return: Similarity of document1 and document2.
        """

        return len(s1.intersection(s2)) / len(s1.union(s2))
