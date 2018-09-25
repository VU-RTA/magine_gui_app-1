import os

import pandas as pd

from data_format.format import process_raptr_zip
from gui.models import Data, EnrichmentOutput
from magine.data.experimental_data import ExperimentalData
from magine.enrichment.enrichr import Enrichr, db_types
from magine_gui_app.settings import BASE_DIR

_dir = BASE_DIR
e = Enrichr()


def add_project(proj_name):
    print('saving {}'.format(proj_name))
    Data.objects.filter(project_name=proj_name).delete()
    new = Data.objects.create(project_name=proj_name)
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__), '{}.csv.gz'.format(proj_name)),
        set_time_point=True,
    )
    new.save()
    print('saved')


def add_project_from_zip(proj_name, filename):
    print('saving {}'.format(proj_name))
    Data.objects.filter(project_name=proj_name).delete()
    new = Data.objects.create(project_name=proj_name)
    print(filename)
    df = process_raptr_zip(filename)

    new.set_exp_data(df, set_time_point=True)

    new.save()
    print('saved')


def dump_project(proj_name):
    data = EnrichmentOutput.objects.filter(project_name=proj_name)
    df = pd.DataFrame(list(data.values()))
    df.to_csv('{}_enrichment_dump.csv.gz'.format(proj_name),
              compression='gzip')

