from triest import TriestBase, TriestImpr
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Mining Data Streams")

    parser.add_argument('path', type=str, help="Required: Path of dataset")
    parser.add_argument('--M', type=int, default=1000, help='Optional: Reservoir size')
    parser.add_argument('-m', '--model', type=str, default='base', help='Optional: Triest Base or Triest Improved')

    args = parser.parse_args()

    DATASET_PATH = args.path
    M = args.M
    MODEL = args.model

    triest_alg = None
    if MODEL == 'base':
        triest_alg = TriestBase(M, DATASET_PATH)
    else:
        triest_alg = TriestImpr(M, DATASET_PATH)
    tau = triest_alg.process()
    print(tau)
