import time
from itertools import combinations


def generate_subsets(input_set):
    all_subsets = []
    for r in range(1, len(input_set)):
        subsets = combinations(input_set, r)
        all_subsets.extend(map(set, subsets))
    return all_subsets


class RuleFinder:
    def __init__(self, ls: list, confidence: float):
        self._ls = ls
        self._confidence = confidence

    def find_rules(self, frequent_sets):
        start_time = time.time()

        confident_rules = list()
        unconfident_rules = list()

        for itemset in frequent_sets:
            support_I = self._ls[len(itemset) - 1][itemset]
            all_subsets = generate_subsets(itemset)
            for subset in all_subsets:
                # first check whether the current subset can be directly determined as unconfident
                flag = False
                for unconf_rule in unconfident_rules:
                    if subset.issubset(unconf_rule):
                        flag = True
                        break
                if flag: continue

                # calculate conf
                if len(subset) == 1:
                    support_A = self._ls[len(subset) - 1][list(subset)[0]]
                else:
                    support_A = self._ls[len(subset) - 1][tuple(sorted(subset))]

                cur_conf = support_I / support_A

                if cur_conf >= self._confidence:  # if confident rules
                    confident_rules.append([tuple(sorted(subset)), tuple(sorted(set(itemset) - subset)), cur_conf])
                else:  # if unconfident rules
                    unconfident_rules.append(subset)

        # visualization
        print("confident rules:")
        for i, sublist in enumerate(confident_rules):
            print(f'rule {i}: {sublist[0]} ===> {sublist[1]}, score: {sublist[2]:.3f}')

        # calculating time cost
        end_time = time.time()
        print(f'time cost for finding confident rules: {end_time - start_time:.3f}')

        return confident_rules
