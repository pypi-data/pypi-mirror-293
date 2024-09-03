# XT-neighbor-cpu

## Description
This is a wrapper Python package for calling SymDel algorithm which is used in finding nearest neighbors of AIRR sequence used in immunological applications. It supports both the CLI and Python API usage. It is mentioned in [XTNeighbor paper](https://arxiv.org/abs/2403.09010) and has its actual implementation in [Pyrepseq package](https://github.com/andim/pyrepseq).

## Installation
```bash
pip install xt-neighbor-cpu
```

## Library Usage
```python
from xt_neighbor_cpu import nearest_neighbor

seqs = ['CAA', 'CAD', 'CDA', 'CKK']
distance_threshold = 1
result = nearest_neighbor(seqs, distance_threshold)
# return [ (0,1,1), (0,2,1) ]
# where each triplet (i,j,d) represents the sequence index i,j and their edit distance d.
```


## Library Documentation
```python
    """
    List all neighboring sequences efficiently within the given distance using SymDel algorithm.
    That is, given a list of AIRR sequences and edit distance threshold, find all pairs of sequences that have their edit distance smaller or equal to the threshold.

    If seqs2 is not provided, every sequences are compared against every other sequences resulting in N(seqs)**2 combinations.
    Otherwise, seqs are compared against seqs2 resulting in N(seqs)*N(seqs2) combinations.

    For more information, see https://arxiv.org/abs/2403.09010.

    Parameters
    ----------
    seqs : iterable of strings
        list of CDR3B sequences
    max_edits : int
        maximum edit distance defining the neighbors
    max_returns : int or None
        maximum neighbor size
    custom_distance : Function(str1, str2) or "hamming"
        custom distance function to use, must statisfy 4 properties of distance (https://en.wikipedia.org/wiki/Distance#Mathematical_formalization)
    max_custom_distance : float
        maximum distance to include in the result, ignored if custom distance is not supplied
    seq2 : iterable of strings or None
        another list of CDR3B sequences to compare against
    progress : bool
        show progress bar

    Returns
    -------
    neighbors : array of 3D-tuples
        neigbors along with their edit distances in format [(x_index, y_index, edit_distance)]
    """
```

## Command Line Usage
```bash
echo "Complimentaty Commands ===="
python -m xt_neighbor_cpu --help
python -m xt_neighbor_cpu --version

echo "Basic Usage ===="
python -m xt_neighbor_cpu -i dummy_input.txt -o output1.txt
python -m xt_neighbor_cpu -i dummy_input.txt -d 2

echo "AIRR Mode ===="
python -m xt_neighbor_cpu -a -i dummy_input_airr.tsv

echo "Comparison Mode ===="
python -m xt_neighbor_cpu -a -i dummy_input_airr.tsv -I dummy_input_airr.tsv -o output2.txt

echo "Hamming Distance Mode ===="
python -m xt_neighbor_cpu -a -i dummy_input_airr.tsv -m hamming
python -m xt_neighbor_cpu -a -i dummy_input_airr.tsv -m hamming -d 2

```
See `test` folder for more information

## Command Line Documentation
```bash
usage: xt_neighbor_cpu [-h] [-d DISTANCE] [-o OUTPUT_PATH] [-m {leven,hamming}] [-v] [-V] [-a] -i INPUT_PATH [-I QUERY_INPUT_PATH]

Perform nearest neighbor search for AIR sequences with the given distance threshold using CPU-based SymDel algorithm

optional arguments:
  -h, --help            show this help message and exit
  -d DISTANCE, --distance DISTANCE
                        distance threshold defining the neighbor (default to 1)
  -o OUTPUT_PATH, --output-path OUTPUT_PATH
                        path of the output file (default to no output)
  -m {leven,hamming}, --measurement {leven,hamming}
                        distance measurement (default to leven)
  -v, --version         print the version of the program then exit
  -V, --verbose         print extra detail as the program runs for debugging purpose
  -a, --airr            use AIRR format for input-path instead. Relevant fields are cdr3_aa and duplicate_count
  -i INPUT_PATH, --input-path INPUT_PATH
                        path of csv input file. It should contain exactly 1 column (AIR sequences) or AIRR-compatible format with
                        -a mode
  -I QUERY_INPUT_PATH, --query-input-path QUERY_INPUT_PATH
                        path of the second csv input file for comparison mode with the same format as -i mode. With this argument,
                        the returning triplets (i,j,d) would have i referencing the first inputs and j referencing the second
                        inputs
```