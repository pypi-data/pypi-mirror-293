from pyrepseq import symdel


def nearest_neighbor(seqs, max_edits=1, custom_distance=None,
                     max_custom_distance=float('inf'), output_type='triplets',
                     seqs2=None, progress=False):
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
    result = symdel(
        seqs, max_edits=max_edits, custom_distance=custom_distance,
        max_custom_distance=max_custom_distance, seqs2=seqs2, progress=progress)
    if seqs2 is not None:
        return result
    return list(filter(lambda x: x[0] < x[1], result))
