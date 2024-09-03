import argparse
import pandas as pd
from .xt_neighbor import nearest_neighbor
import sys
from os import path
import re


def get_version():
    filename = path.join(path.dirname(__file__), '../../pyproject.toml')
    with open(filename) as file:
        return re.search(r'version\s*=\s*"([^"]+)"',file.read()).group(1)
    return 'null'


def get_args():
    parser = argparse.ArgumentParser(
        prog='xt_neighbor_cpu', description=(
            'Perform nearest neighbor search for AIR sequences with'
            ' the given distance threshold using CPU-based SymDel algorithm'))
    parser.add_argument('-d', '--distance', type=int, default=1,
                        help='distance threshold defining the neighbor (default to 1)')
    parser.add_argument('-o', '--output-path',
                        help='path of the output file (default to no output)')
    parser.add_argument('-m', '--measurement',
                        choices=['leven', 'hamming'], default='leven',
                        help='distance measurement (default to leven)')
    parser.add_argument('-v', '--version', action='version',
                        version=f'xt_neighbor_cpu {get_version()}')
    parser.add_argument('-V', '--verbose', action='store_true', help=(
        'print extra detail as the program runs for debugging purpose'))
    parser.add_argument('-a', '--airr', action='store_true', help=(
        'use AIRR format for input-path instead.'
        ' Relevant fields are cdr3_aa and duplicate_count'))
    parser.add_argument('-i', '--input-path', required=True, help=(
        'path of csv input file. It should contain'
        ' exactly 1 column (AIR sequences) or AIRR-compatible format with -a mode'))
    parser.add_argument('-I', '--query-input-path', help=(
        'path of the second csv input file for comparison mode with the same format as'
        ' -i mode. With this argument, the returning triplets (i,j,d) would have i'
        ' referencing the first inputs and j referencing the second inputs'))
    return parser.parse_args()


def read_file(filepath, airr=False):
    separator = '\t' if airr else ','
    cols = ['cdr3_aa'] if airr else [0]
    df = pd.read_csv(filepath, usecols=cols, sep=separator)
    return df.iloc[:, 0].tolist()


def write_file(filepath, data):
    with open(filepath, 'w') as file:
        for triplet in data:
            file.write(f'{triplet[0]} {triplet[1]} {triplet[2]}\n')


def print_exit(message):
    print(message, file=sys.stderr)
    sys.exit(1)


def main():
    args = get_args()
    if args.verbose:
        print(args)

    # run
    measure = 'hamming' if args.measurement == 'hamming' else None
    seqs = read_file(args.input_path, args.airr)
    seqs2 = read_file(args.query_input_path,
                      args.airr) if args.query_input_path else None
    result = nearest_neighbor(seqs, args.distance, measure,
                              seqs2=seqs2, progress=args.verbose)

    # finish up
    if args.output_path is not None:
        write_file(args.output_path, result)
    print(f'Success! number of returns: {len(result)}')


main()
