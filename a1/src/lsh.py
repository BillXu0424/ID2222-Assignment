import numpy as np
from typing import Set, Tuple, List
import itertools
from compareSets import CompareSets


class LSH:
    def __init__(self, t: float = 0.8, band: int = 20) -> None:
        """
        Initialize LSH processor, in order to find candidate pairs, and for later real similar pairs search.
        :param t: similarity threshold
        :param band: band size for LSH
        """

        self._t = t
        self._band = band

    def find_candidate_pairs(self, sig_matrix: np.ndarray) -> Set[Tuple[int, int]]:
        """
        Find candidate pairs of documents.
        :param sig_matrix: Signature matrix, an (n*d) np.ndarray,
        where n is the number of hash function, d is the number of documents
        :return: A set of candidate pairs.
        """

        n_rows, n_docs = sig_matrix.shape
        candidate_pairs = set()

        for band_start in range(0, n_rows, self._band):
            buckets = dict()
            portions = sig_matrix[band_start: band_start + self._band, :]
            for i in range(n_docs):
                portion = portions[:, i]
                key = "_".join(portion.astype(str))
                if key in buckets.keys():
                    buckets[key].add(i)
                else:
                    buckets[key] = {i}

            for doc_set in buckets.values():
                if len(doc_set) > 1:
                    candidate_pairs.update(set(itertools.combinations(doc_set, 2)))

        return candidate_pairs

    def find_sim_pairs(self, candidate_pairs: Set[Tuple[int, int]], shinglesList: List[Set[int]]) -> Set[Tuple[int, int]]:
        """
        Filter real similar pairs from candidate pairs.
        :param candidate_pairs: Candidate pairs.
        :param shinglesList: A list of document shingles.
        :return: A set of real similar pairs.
        """

        sim_pairs = set()
        for candidate_pair in candidate_pairs:
            shingles1 = shinglesList[candidate_pair[0]]
            shingles2 = shinglesList[candidate_pair[1]]
            if CompareSets.sim(shingles1, shingles2) > self._t:
                sim_pairs.add(candidate_pair)

        return sim_pairs
