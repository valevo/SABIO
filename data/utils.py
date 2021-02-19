import glob
from tqdm import tqdm

from collections import defaultdict
from itertools import groupby
import numpy.random as rand
import pandas as pd

import rdflib
from rdflib import Graph


def load_RDF_from_dir(d, until=-1, file_ext="rdf", randomise=False):
    file_listing = glob.glob(f"{d}/*.{file_ext}")
    file_listing = rand.permutation(file_listing) if randomise else sorted(file_listing)
    file_listing = file_listing[:until] # there are 1570 files in /objects, loop below has 1.5 it/s so takes 15+min
    
    if len(file_listing) == 0:
        raise ValueError(f"taking {until} files from directory /{d}/ somehow not possible, listing empty!")
    
    graph = Graph()
    for path in tqdm(file_listing, 
                     desc=f"Parsing{' random' if randomise else ''} files from /{d}"): 
        graph.parse(path, format="xml")
    return graph



def put(d, k, v):
    if not k in d:
        d[k] = v
    else:
        try:
            d[k] = (*d[k], v)
        except AttributeError:
            d[k] = (d[k], v)


def unpack_or_cast_values(d):
    return {k: (v[0] if len(v) == 1 else tuple(v)) for k, v in d.items()}


def triples_to_record(group_name, group, qname=lambda x:x):
    record = defaultdict(list)
    record["object_URI"].append(group_name)
    
    for s, p, o in group:
        p = qname(p)
        try:
            o = qname(o)
        except ValueError: # object was of type Literal
            o = str(o)
        record[p].append(o)
    return unpack_or_cast_values(record)


def graph_to_df(graph, qname=lambda x:x):
    grouped = groupby(sorted(graph), lambda triple: triple[0])
    records = [triples_to_record(k, group, qname=qname) for k, group in tqdm(grouped)]
    return pd.DataFrame.from_records(records)
    
    