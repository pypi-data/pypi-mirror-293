from pyrepseq import symdel


def nearest_neighbor(seqs, max_edits=1, max_returns=None,
             custom_distance=None, max_custom_distance=float('inf'),
             output_type='triplets', seqs2=None, progress=False):
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
    output_type: string
        format of returns, can be "triplets", "coo_matrix", "ndarray"
    seq2 : iterable of strings or None
        another list of CDR3B sequences to compare against
    progress : bool
        show progress bar

    Returns
    -------
    neighbors : array of 3D-tuples, sparse matrix, or dense matrix
        neigbors along with their edit distances according to the given output_type
        if "triplets" returns are [(x_index, y_index, edit_distance)]
        if "coo_matrix" returns are scipy's sparse matrix where C[i,j] = distance(X_i, X_j) or 0 if not neighbor
        if "ndarray" returns numpy's 2d array representing dense matrix
    """
	return symdel(seqs, max_edits, max_returns, custom_distance, max_custom_distance,
             output_type, seqs2, progress)