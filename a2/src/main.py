from apriori import Apriori
from find_rules import RuleFinder
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Discovery of Frequent Itemsets and Association Rules")

    parser.add_argument('-path', type=str, default='../dataset/T10I4D100K.dat', help="Required: Path of dataset")
    parser.add_argument('-s', '--support', type=float, default=0.01, help='Optional: Threshold of support')
    parser.add_argument('-c', '--confidence', type=float, default=0.5, help='Optional: Threshold of confidence')

    args = parser.parse_args()

    DATASET_PATH = args.path
    SUPPORT = args.support
    CONFIDENCE = args.confidence

    apriori = Apriori(SUPPORT, DATASET_PATH)
    ls = apriori.proceed()
    for i, l in enumerate(ls):
        print(f"i: {i + 1}, length: {len(l)}")
        print("## display ##")
        print(l.keys())

    frequent_sets = apriori.generate_frequent_sets(ls)
    print(frequent_sets)

    rule_finder = RuleFinder(ls, confidence=CONFIDENCE)
    rules = rule_finder.find_rules(frequent_sets)