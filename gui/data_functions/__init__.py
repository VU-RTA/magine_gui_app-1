import pandas as pd
import numpy as np
from magine.data.datatypes import create_table_of_data
fold_change = 'treated_control_fold_change'
flag = 'significant_flag'
exp_method = 'data_type'
p_val = 'p_value_group_1_and_group_2'
rna = 'rna_seq'
gene = 'gene'
protein = 'protein'
metabolites = 'metabolites'
species_type = 'species_type'
sample_id = 'time'


def get_significant_numbers(data, sig, unique):
    """

    Parameters
    ----------
    data : pd.DataFrame

    Returns
    -------

    """

    t = create_table_of_data(data, sig=sig, unique=unique)
    t = t.replace('-', np.nan)
    t_dict = t.to_dict()
    new_dict = dict()
    for time, i in t_dict.items():
        for key, value in i.items():
            if value not in (np.nan, 'Total Unique Across'):
                if np.isfinite(value):
                    value = int(value)
            if key in new_dict:

                new_dict[key][time] = value
            else:
                new_dict[key] = dict()
                new_dict[key][time] = value
    # print(new_dict)
    times = []
    for i in t_dict.keys():
        if not isinstance(i, str):
            i = float(i)
        times.append(i)
    times = [str(i) for i in times]
    return times, new_dict


def get_all_tables(data):
    time, all_measured = get_significant_numbers(data, unique=False, sig=False)
    time, uni_measured = get_significant_numbers(data, unique=True, sig=False)
    time, sig_measured = get_significant_numbers(data, unique=False, sig=True)
    time, sig_uni = get_significant_numbers(data, unique=True, sig=True)
    return time, all_measured, uni_measured, sig_measured, sig_uni


if __name__ == '__main__':
    df = pd.read_csv(r'C:\Users\James Pino\PycharmProjects\magine_gui_app\gui\\test_data\data.csv.gz',
                     low_memory=False)
    print(get_significant_numbers(df,True, True))
