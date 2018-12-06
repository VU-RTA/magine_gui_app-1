import numpy as np
import pandas as pd

from magine.mappings.chemical_mapper import ChemicalMapper

try:
    basestring
# Allows isinstance(foo, basestring) to work in Python 3
except:
    basestring = str

from .utils import load_from_zip
from .standard_cols import *

cm = ChemicalMapper()

rename_met_dict = {
    'max_fold_change_treated_vs_control': fold_change,
    'significant_flag': flag,
    "anova_p": p_val,
    'phase': exp_method,
    "experiment_type": species_type,
    'compound_id': identifier,
    'name': label,
    'time_points': sample_id,

}


def process_metabolites(filename):
    data = load_from_zip(filename)

    data.loc[:, label] = data.apply(merge_metabolite_row, axis=1)
    data.loc[:, exp_method] = data['phase']
    data.loc[:, identifier] = data['compound_id']
    data.loc[:, flag] = data['significant_flag']
    data.loc[:, p_val] = data['anova_p']
    data.loc[:, species_type] = data['experiment_type']
    data.loc[:, sample_id] = data['time_points']
    data.loc[:, fold_change] = data['max_fold_change_treated_vs_control']

    idx = data.groupby(['compound'])['score'].transform(max) == data['score']

    data.loc[:, 'top_score'] = False
    data.loc[idx, 'top_score'] = True

    data[fold_change] = data[fold_change].apply(pd.to_numeric, errors='coerce')

    data = data.loc[np.isfinite(data[fold_change])]
    data.loc[data[fold_change] == np.inf, fold_change] = 1000.
    data.loc[data[fold_change] == -np.inf, fold_change] = -1000.

    data.loc[:, label] = data[label].astype(basestring)
    data.loc[:, identifier] = data.apply(update_hmdb, axis=1)
    return data


def merge_metabolite_row(row):
    """ compresses metabolite information columns

    For the metabolite data, we want to minimize the number of columns.
    We check to see if the "name" row exists, if it doesn't, we check to see
    if "description" row exists, if not we default to "compound_id".

    This compresses the redundant information stored in "name", "description",
    and "compound_id".

    Parameters
    ----------
    row

    Returns
    -------

    """
    if not isinstance(row['name'], basestring):
        if isinstance(row['description'], basestring):
            row['name'] = row['description']
        else:
            row['name'] = row['compound_id']
    return row['name']


def update_hmdb(row):
    current = row[identifier]
    if current.startswith('HMDB'):
        if current in cm.hmdb_accession_to_main:
            return cm.hmdb_accession_to_main[current][0]
    return current
