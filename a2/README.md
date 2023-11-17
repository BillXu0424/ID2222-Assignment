# Homework 2: Discovery of Frequent Itemsets and Association Rules

This homework is aimed at discovering association rules between itemsets in a sales transaction database (a set of baskets) includes the following two sub-problems:

1. Finding frequent itemsets with support at least ***s***;
2. Generating association rules with confidence at least ***c*** from the itemsets found in the first step.

The homework is implemented with Python.

## Run

```bash
python main.py ../ dataset/T10I4D100K.dat -s 0.005 -c 0.5
```

- required positional argument: path of dataset.

- `-s` / `--support`: Threshold of support

- `-c` / `--confidence`: Threshold of confidence


