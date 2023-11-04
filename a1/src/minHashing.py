import random
import numpy as np
from typing import Set, List, Tuple


class MinHashing:
    def __init__(self, n_hash_func: int, max_hash: int, hash_rules: List[Tuple[int, int]] = None) -> None:
        """
        Initialize a min-hasher, which is used to generate a signature for a document shingles.
        :param n_hash_func: Hyperparameter. The number of hash functions used.
        :param max_hash: Maximum index of a shingle.
        :param hash_rules: Optional, randomly generate hashing rules if None is passed.
        The length of hash_rules must be equal to n_hash_func. Each term is (a, b),
        which indicates the hashing rule is (a * shingle + b) % max_hash.
        """

        self._n_hash_func = n_hash_func
        self._max_hash = max_hash

        self._hash_rules = list()
        if hash_rules is None:
            self._gen_hash_rules()
        else:
            if len(hash_rules) != self._n_hash_func:
                raise "Length of hash_rules is not equal to h_hash_func!"
            else:
                self._hash_rules = hash_rules

    def _gen_hash_rules(self):
        """
        Generate n_hash_func hashing rules randomly.
        :return: A list of hashing rules.
        """

        for _ in range(self._n_hash_func):
            self._hash_rules.append((random.randint(1, self._max_hash), random.randint(1, self._max_hash)))

    def gen_sig(self, shingles: Set[int]) -> np.ndarray:
        """
        Generate a signature for a single document.
        :param shingles: Shingles of a document.
        :return: The signature of a document.
        """

        signature = np.ones(self._n_hash_func).astype(int) * self._max_hash
        for shingle in shingles:
            temp_hashes = np.zeros(self._n_hash_func).astype(int)
            for i, (a, b) in enumerate(self._hash_rules):
                temp_hashes[i] = (a * shingle + b) % self._max_hash
            signature = np.minimum(signature, temp_hashes)

        return signature


if __name__ == '__main__':
    hash_rules = [(1, 1), (3, 1)]
    min_hasher = MinHashing(2, 5, hash_rules)
    shinglesList = [{0, 3}, {2}, {1, 3, 4}, {0, 2, 3}]
    for shingles in shinglesList:
        print(min_hasher.gen_sig(shingles))
