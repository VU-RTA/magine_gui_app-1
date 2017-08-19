import os
import sys
import pandas as pd
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magine_gui_app.settings')
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)

from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from gui.models import Data, Measurement, EnrichmentOutput


def add_cisplatin():

    Data.objects.all().delete()

    new = Data.objects.create(project_name='cisplatin_test')
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__),
                     'norris_et_al_2017_cisplatin_data.csv.gz')
    )
    new.save()


def add_meth():
    print('saving methotrexate')
    there = Data.objects.all()
    there.filter(project_name='methotrexate')
    if len(there) > 0:
        there.delete()

    new = Data.objects.create(project_name='methotrexate')
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__),
                     'data.csv.gz')
    )
    new.save()
    print(new.get_time_points())
    print('saved')


def add_enrichment():
    from magine.ontology.enrichr import Enrichr
    from magine.data.datatypes import ExperimentalData
    EnrichmentOutput.objects.all().delete()
    e = Enrichr()
    d = Data.objects.all()
    meth = d.filter(project_name='methotrexate')[0]
    exp = ExperimentalData(meth.data)

    for genes, sample_id in zip(exp.proteomics_up_over_time, exp.proteomics_time_points):
        df = e.run_set_of_dbs(genes, db='pathways')
        dict_list = df.to_dict(orient='records')
        for i in dict_list:

            m = EnrichmentOutput.objects.create(
                project_name='methotrexate',
                sample_id=sample_id,
                **i)
            m.save()


def add_project_measurements():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                     'norris_et_al_2017_cisplatin_data.csv.gz'),
                     low_memory=False)

    df = df[~df['treated_control_fold_change'].isnull()]

    project_name = 'Cisplatin'

    def add_from_row(row):

        tmp_dict = dict(row)
        tmp_dict['sample_id'] = tmp_dict['time']
        tmp_dict['project_name'] = project_name
        tmp_dict.pop('time_points', None)
        tmp_dict.pop('time', None)
        m = Measurement(**tmp_dict)
        m.save()

    df.apply(add_from_row, axis=1)

if __name__ == '__main__':
    # add_cisplatin()
    # add_project_measurements()
    # add_meth()
    add_enrichment()
