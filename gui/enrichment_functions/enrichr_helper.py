import pandas as pd
import os
import sys

from magine.ontology.enrichr import Enrichr
from magine.html_templates.html_tools import create_yadf_filters
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magine_gui_app.settings')
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from magine_gui_app.settings import BASE_DIR
_dir = BASE_DIR

e = Enrichr()


cols = ['term_name', 'combined_score', 'adj_p_value', 'rank',  'genes',
        'n_genes', 'sample_id', 'db']


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

    def _add_check(row):
        i = row.name
        out = '<input type="checkbox" id="checkbox{0}" name="rowcheckbox"> ' \
              '<label for="checkbox{0}"></label>'.format(i)
        return out

    tmp_table['checkbox'] = tmp_table.apply(_add_check, axis=1)
    return tmp_table


def model_to_json(model):
    df = pd.DataFrame(list(model))
    if 'id' in df.columns:
        del df['id']
    if 'project_name' in df.columns:
        del df['project_name']
    tmp_table = _format_simple_table(df)
    cols.append('checkbox')
    tmp_table = tmp_table[cols]
    d = create_yadf_filters(tmp_table)
    data = tmp_table.to_dict('split')
    data['filters'] = d
    template_vars = {"data": data}
    return template_vars


def return_table(list_of_genes, ont='pathways'):
    cols = ['term_name', 'combined_score', 'adj_p_value', 'rank',
            'genes', 'n_genes', 'db']
    df = e.run_set_of_dbs(list_of_genes, db=ont)[cols]
    tmp_table = _format_simple_table(df)
    tmp_table['genes'] = tmp_table['genes'].str.split(',').str.join(', ')
    d = create_yadf_filters(tmp_table)
    data = tmp_table.to_dict('split')

    data['filters'] = d
    template_vars = {"data": data}
    return template_vars


def return_table_from_model(project_name, category, dbs):
    from gui.models import EnrichmentOutput
    cols = ['term_name', 'combined_score', 'adj_p_value', 'rank', 'genes',
            'n_genes', 'sample_id', 'db', 'category']
    if len(project_name) > 1:
        cols.insert(0, 'project_name')

    df = EnrichmentOutput.objects.all().filter(project_name__in=project_name)
    df = df.filter(category__in=category)
    df = df.filter(db__in=dbs)
    df = pd.DataFrame(list(df.values()))[cols]
    df = df[df['adj_p_value'] < 0.2]
    tmp_table = _format_simple_table(df)
    tmp_table['genes'] = tmp_table['genes'].str.split(',').str.join(', ')
    d = create_yadf_filters(tmp_table)
    data = tmp_table.to_dict('split')
    data['filters'] = d
    template_vars = {"data": data}
    return template_vars


if __name__ == '__main__':
    return_table(['BAX', 'BCL2', 'MCL1', 'CASP3', 'CASP8'])

