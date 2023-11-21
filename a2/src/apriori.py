from itertools import combinations
from tqdm import tqdm
from collections import Counter
import time


class Apriori:
    def __init__(self, s: float, input: str):
        self._s = s
        self._input = input
        self._read_input()

    def _read_input(self):
        self._baskets = list()
        with open(self._input, "r") as f:
            for line in f:
                items = set(map(lambda a: int(a), line.strip().split(' ')))
                self._baskets.append(items)
        self._s = int(self._s * len(self._baskets))

    def proceed(self):
        start_time = time.time()

        l1 = dict()
        for items in self._baskets:
            for item in items:
                l1[item] = l1.get(item, 0) + 1

        l1 = {key: value for key, value in l1.items() if value >= self._s}

        ls = list()
        ls.append(l1)

        c = set(combinations(set(l1.keys()), 2))

        i = 2

        while len(c) > 0:
            l = Counter(
                [
                    item_set
                    for basket in self._baskets
                    for item_set in tuple(combinations(sorted(basket), i))
                    if item_set in c
                ]
            )

            l = {key: value for key, value in l.items() if value >= self._s}
            if len(l) == 0:
                break
            ls.append(l)

            c = set()
            for k_tuple in tqdm(l.keys()):
                for ele in l1.keys():
                    if ele not in k_tuple:
                        new_tuple = tuple(sorted(k_tuple + (ele,)))
                        c.add(new_tuple)

            i += 1

        end_time = time.time()
        print(f'time cost for finding frequent item sets: {end_time - start_time:.3f}')
        return ls

    @staticmethod
    def generate_frequent_sets(ls):
        frequent_sets = list()
        for l in ls[1:]:
            frequent_sets.extend(list(l.keys()))
        frequent_sets.reverse()
        return frequent_sets


if __name__ == '__main__':
    apriori = Apriori(0.01, '../dataset/T10I4D100K.dat')
    ls = apriori.proceed()
    print(ls)
