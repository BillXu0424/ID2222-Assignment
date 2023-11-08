import itertools
import numpy as np
import argparse
import time

from textLoader import TextLoader
from shingling import Shingling
from minHashing import MinHashing
from lsh import LSH
from compareSets import CompareSets
from compareSignatures import CompareSignatures

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser(description="Finding Similar Items: Textually Similar Documents")

    parser.add_argument('path', type=str, help="Required: Path of corpus")
    parser.add_argument('--k', type=int, default=5, help='Optional: Length of a single shingle')
    parser.add_argument('--n', type=int, default=500, help='Optional: Number of hash functions in signature')
    parser.add_argument('-m', '--mod', type=int, default=10 ** 9 + 7, help='Optional: Maximum number of hash')
    parser.add_argument('-t', '--threshold', type=float, default=0.1, help='Optional: Threshold of being similar')
    parser.add_argument('-b', '--band', type=int, default=20, help='Optional: Band width in LSH')

    args = parser.parse_args()

    DATASET_PATH = args.path
    K = args.k
    N_HASH_FUNC = args.n
    MAX_HASH = args.mod
    THRESHOLD = args.threshold
    BAND = args.band

    # load data
    textLoader = TextLoader(DATASET_PATH)
    data_dic = textLoader.load_text()

    # init
    sl = Shingling(K)
    mh = MinHashing(N_HASH_FUNC, MAX_HASH)

    # shingling and calculate Jaccard sim, minHashing and calculate Signatures sim
    order = set(itertools.combinations(data_dic.keys(), 2))

    shingling_result = {}
    minHashing_result = {}

    part1_start = time.time()

    for item in order:
        data1, data2 = item

        sl_set_1, sl_set_2 = sl.get_shingling_set(data_dic[data1]), sl.get_shingling_set(data_dic[data2])
        shingling_result[f'{data1} & {data2}'] = CompareSets.sim(sl_set_1, sl_set_2)

        minHashing_result[f'{data1} & {data2}'] = CompareSignatures.sim(mh.gen_sig(sl_set_1), mh.gen_sig(sl_set_2))

    part1_end = time.time()

    shingling_result = sorted(shingling_result.items(), key=lambda x: x[1], reverse=True)
    print(f'Jaccard sim of {K} shinglings:\n{shingling_result}\n\n\n')

    minHashing_result = sorted(minHashing_result.items(), key=lambda x: x[1], reverse=True)
    print(f'Signatures sim:\n{minHashing_result}\n\n\n')

    # LSH
    doc_idx = {}
    sl_list = []
    sig_list = []
    i = 0

    lsh_start = time.time()

    lsh = LSH(t=0.1, band=5)

    for data_name, text in data_dic.items():  # build signature matrix
        sl_set = sl.get_shingling_set(data_dic[data_name])
        sig = mh.gen_sig(sl_set)
        sl_list.append(sl_set)
        sig_list.append(sig)

        doc_idx[i] = data_name
        i += 1

    sig_matrix = np.vstack(sig_list).T

    candidate_pairs = lsh.find_candidate_pairs(sig_matrix)
    candidate_pairs_name = set()
    for tp in candidate_pairs:
        candidate_pairs_name.add((doc_idx[tp[0]], doc_idx[tp[1]]))

    lsh_end = time.time()

    print(f'Candidate pairs:{candidate_pairs_name}')

    sim_pairs = lsh.find_sim_pairs(candidate_pairs, sl_list)
    sim_pairs_name = set()
    for tp in sim_pairs:
        sim_pairs_name.add((doc_idx[tp[0]], doc_idx[tp[1]]))

    print(f'Sim pairs:{sim_pairs_name}\n')

    print(f'time cost for calculating shingling and minHashing: {part1_end - part1_start:.3f}')
    print(f'time cost for LSH: {lsh_end - lsh_start:.3f}\n')
