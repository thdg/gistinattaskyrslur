"""
Map regional codes to name
"""


R2N_DATA = "utils/r2n.tsv"


def _load_r2n_map(fname):
    r2n = dict()
    with open(fname) as fin:
        for line in fin:
            k, v = line.split("\t")
            r2n[k] = v.strip()
    return r2n

R2N = _load_r2n_map(R2N_DATA)

