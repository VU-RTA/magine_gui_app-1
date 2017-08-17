from magine.ontology.enrichr import Enrichr

e = Enrichr()

range_number = 'column_number:{},' \
               'filter_type: "range_number"'

auto_complete = 'column_number:{},' \
                'filter_type: "auto_complete",' \
                'text_data_delimiter: ","'

chosen = 'column_number:{}, ' \
         'filter_type: "multi_select",' \
         'select_type: "select2",' \
         'select_type_options: {{width: \'150px\'}}, ' \
         'text_data_delimiter: ","'

html_selector = 'column_number:{},' \
                'column_data_type: "html",' \
                'filter_type: "multi_select",' \
                'select_type: "chosen"'

# GO
dict_of_templates = dict(GO_id=range_number,
                         GO_name=chosen,
                         slim=chosen,
                         aspect=chosen,
                         ref=range_number,
                         depth=range_number,
                         enrichment_score=range_number,
                         term_name=chosen,
                         term_id=chosen,
                         rank=range_number,
                         p_value=range_number,
                         adj_p_value=range_number,
                         combined_score=range_number,
                         genes=chosen,
                         n_genes=range_number,
                         z_score=range_number,
                         significant_flag=chosen,
                         data_type=chosen,
                         pvalue=range_number,
                         treated_control_fold_change=range_number,
                         p_value_group_1_and_group_2=range_number,
                         protein=auto_complete,
                         gene=chosen,
                         time=chosen,
                         compound=auto_complete,
                         compound_id=auto_complete,
                         db=chosen,

                         )


def yadf_filter(table):
    n = 0
    out_string = ''
    for n, i in enumerate(table.index.names):
        if i not in dict_of_templates:
            continue
        new_string = dict_of_templates[i].format(n)
        out_string += '{' + new_string + '},\n'

    for m, i in enumerate(table.columns):

        if isinstance(i, str):
            new_string = dict_of_templates[i].format(n + m)
            out_string += '{' + new_string + '},\n'
            continue
        elif i not in dict_of_templates:
            continue
        new_string = dict_of_templates[i[0]].format(n + m)
        out_string += '{' + new_string + '},\n'
    return out_string


def _format_simple_table(data):
    """
    formats precession of data for outputs

    Parameters
    ----------
    data : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame, dict
    """
    tmp_table = data.copy()
    pvalue_float_type = ['pvalue', 'p_value', 'p_value_group_1_and_group_2',
                         'adj_p_value']

    float_type = ['z_score', 'combined_score', 'enrichment_score',
                  'treated_control_fold_change']

    int_type = ['n_genes', 'rank']

    for i in data.columns:
        if i in float_type:
            tmp_table[i] = tmp_table[i].fillna(0)
            tmp_table[i] = tmp_table[i].astype(float)
            tmp_table[i] = tmp_table[i].round(2)
            tmp_table[i] = tmp_table[i].apply('{:.4g}'.format)
        elif i in pvalue_float_type:
            tmp_table[i] = tmp_table[i].fillna(1)
            tmp_table[i] = tmp_table[i].apply('{:.2g}'.format)
        elif i in int_type:

            tmp_table[i] = tmp_table[i].fillna(0)
            tmp_table[i] = tmp_table[i].astype(int)
            tmp_table[i] = tmp_table[i].apply('{:,d}'.format)

    return tmp_table


def return_table(list_of_genes, ont):
    df = e.run_set_of_dbs(list_of_genes, db=ont)
    tmp_table = _format_simple_table(df)
    tmp_table['genes'] = tmp_table['genes'].str.split(',').str.join(', ')
    d = yadf_filter(tmp_table)
    data = tmp_table.to_dict('split')
    data['filters'] = d
    template_vars = {"data": data}
    return template_vars


if __name__ == '__main__':
    return_table(['BAX', 'BCL2', 'MCL1', 'CASP3', 'CASP8'])


