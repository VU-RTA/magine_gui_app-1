import pandas as pd
import numpy as np

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
    # data_types = data['data_type'].unique()
    tmp_data = data.copy()
    exp_methods = data[exp_method].unique()

    if sig:
        tmp_data = tmp_data[tmp_data[flag]]
    meta_d = tmp_data[tmp_data[species_type] == metabolites].copy()

    exp_methods_metabolite = meta_d[exp_method].unique()

    do_metab = True
    if len(meta_d) == 0:
        do_metab = False

    gene_d = tmp_data[tmp_data[species_type] == protein].copy()

    if unique:
        if do_metab:
            tmp_data1 = meta_d.pivot_table(values='compound',
                                           index=exp_method, columns='time',
                                           aggfunc=lambda x:
                                           x.dropna().nunique())

        tmp_data2 = gene_d.pivot_table(values='gene', index=exp_method,
                                       columns='time',
                                       aggfunc=lambda x:
                                       x.dropna().nunique())

        unique_col = []
        for i in exp_methods:
            if i in exp_methods_metabolite:
                n = len(tmp_data[tmp_data[exp_method] == i][
                            'compound'].dropna().unique())
            else:
                n = len(tmp_data[tmp_data[exp_method] == i][
                            'gene'].dropna().unique())
            unique_col.append(int(n))
    else:
        if do_metab:
            tmp_data1 = meta_d.pivot_table(values='compound_id',
                                           index=exp_method,
                                           columns='time',
                                           aggfunc=lambda x:
                                           x.dropna().nunique())
        tmp_data2 = gene_d.pivot_table(values='protein', index=exp_method,
                                       columns='time',
                                       aggfunc=lambda x:
                                       x.dropna().nunique())
        unique_col = []
        for i in exp_methods:
            if i in exp_methods_metabolite:
                n = len(tmp_data[tmp_data[exp_method] == i][
                            'compound_id'].dropna().unique())
            else:
                n = len(tmp_data[tmp_data[exp_method] == i][
                            'protein'].dropna().unique())
            unique_col.append(int(n))
    if do_metab:
        t = pd.concat([tmp_data1, tmp_data2])
    else:
        t = tmp_data2.fillna('-')

    t['Total Unique Across'] = pd.Series(unique_col, index=t.index)
    t_dict = t.to_dict()
    new_dict = dict()
    for time, i in t_dict.items():
        for key, value in i.items():
            if value not in (np.nan, 'Total Unique Across'):
                value = float(value)
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
    return new_dict, times

if __name__ == '__main__':
    df = pd.read_csv('/home/pinojc/PycharmProjects/magine_gui_app/gui/test_data/norris_et_al_2017_cisplatin_data.csv.gz',
                     low_memory=False)
    print(get_significant_numbers(df,True, True))
