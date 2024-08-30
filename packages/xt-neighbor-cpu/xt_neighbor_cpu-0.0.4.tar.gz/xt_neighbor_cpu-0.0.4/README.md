# XT-neighbor-cpu

## Description
This is a wrapper Python package for calling SymDel algorithm which is used in finding nearest neighbors of AIRR sequence used in immunological applications. It is mentioned in [XTNeighbor paper](https://arxiv.org/abs/2403.09010) and has its actual implementation in [Pyrepseq package](https://github.com/andim/pyrepseq).

## Installation
```bash
pip install xt-neighbor-cpu
```

## Quick Usage
```python
from xt_neighbor_cpu import nearest_neighbor

seqs = ['CAA', 'CAD', 'CDA', 'CKK']
distance_threshold = 1
result = nearest_neighbor(seqs, distance_threshold)
# return [ (0,1,1), (0,2,1) ]
# where each triplet (i,j,d) represents the sequence index i,j and their edit distance d.
```

## Documentation
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
