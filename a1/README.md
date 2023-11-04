# Homework 1: Finding Similar Items: Textually Similar Documents

This homework is aimed at implementing the stages of finding textually similar documents based on Jaccard similarity using the *shingling*, *minhashing*, and *locality-sensitive hashing* (LSH) techniques and corresponding algorithms.

The homework is implemented with Python.

## Run

```bash
python main.py ../corpus_test --k 5 --n 500 -m 1000000007 -t 0.1 -b 20
```

**Arguments:**

- required positional argument: path of corpus

- `--k`: Length of a single shingle (k-shingle)

- `--n`: Number of hash functions in signature

- `-m`/`--mod`: Maximum number of hash

- `-t`/`--threshold`: Threshold of being similar

- `-b`/`--band`: Band width in LSH


