import os
import sys

import pandas as pd
from django.core.wsgi import get_wsgi_application

from data_format.format import process_raptr_zip
from magine.enrichment.enrichr import Enrichr, db_types

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magine_gui_app.settings')
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)


get_wsgi_application()

from gui.models import Data, EnrichmentOutput
from magine_gui_app.settings import BASE_DIR

_dir = BASE_DIR
e = Enrichr()


def add_project(proj_name):
    print('Adding project data\n\t{}'.format(proj_name))
    Data.objects.filter(project_name=proj_name).delete()
    new = Data.objects.create(project_name=proj_name)
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__), '{}.csv.gz'.format(proj_name)),
        set_time_point=True,
    )
    new.save()
    print('Done adding project data')


def dump_project(proj_name):
    data = EnrichmentOutput.objects.filter(project_name=proj_name)
    df = pd.DataFrame(list(data.values()))
    print(df['sample_id'].unique())
    print(df['category'].unique())
    df.to_csv('{}_enrichment_dump.csv.gz'.format(proj_name),
              compression='gzip')


def load_project(proj_name):

    df = pd.read_csv('{}_enrichment_dump.csv.gz'.format(proj_name),
                     index_col=0)

    already_there = set()
    for i in EnrichmentOutput.objects.filter(project_name=proj_name):
        already_there.add("_".join(
            [i.db, i.category, i.sample_id, proj_name])
        )
    dict_list = df.to_dict(orient='records')

    to_add = [EnrichmentOutput(**row) for row in dict_list if
              "_".join([row['db'], row['category'], row['sample_id'],
                        row['project_name']]) not in already_there]
    if len(to_add) != 0:
        EnrichmentOutput.objects.bulk_create(to_add)


def add_project_from_zip(proj_name, filename):
    print('saving {}'.format(proj_name))
    Data.objects.filter(project_name=proj_name).delete()
    new = Data.objects.create(project_name=proj_name)
    print(filename)
    df = process_raptr_zip(filename)

    new.set_exp_data(df, set_time_point=True)

    new.save()
    print('saved')


def add_enrichment(project_name, reset_data=False):
    standard_dbs = []
    for i in ['drug', 'disease', 'ontologies', 'pathways', 'transcription',
              'kinases', 'histone', 'cell_type']:
        standard_dbs += db_types[i]

    if reset_data:
        EnrichmentOutput.objects.filter(project_name=project_name).delete()

    # data = Data.objects.filter(project_name=project_name)[0]
    # exp_data = ExperimentalData(data.data)
    exp_data = Data.return_magine_data(Data, project_name=project_name)

    already_there = set()
    for i in EnrichmentOutput.objects.filter(project_name=project_name):
        already_there.add("{}-{}-{}-{}".format(str(i.db), str(i.category),
                                               str(i.sample_id), project_name))

    def _run(samples, timepoints, category):
        for genes, sample_id in zip(samples, timepoints):
            print(sample_id)
            for i in standard_dbs:
                current = "{}-{}-{}-{}".format(str(i), str(category),
                                               str(sample_id), project_name)
                if current in already_there:
                    continue

                df = e.run(genes, i)
                df['db'] = i
                df['sample_id'] = sample_id
                df['category'] = category
                df['project_name'] = project_name
                dict_list = df.to_dict(orient='records')
                list_to_save = [EnrichmentOutput(**row) for row in dict_list]
                EnrichmentOutput.objects.bulk_create(list_to_save)

    pt = exp_data.proteins.sample_ids
    rt = exp_data.rna.sample_ids

    if len(pt) != 0:
        _run(exp_data.proteins.sig.by_sample, pt, 'proteomics_both')
        _run(exp_data.proteins.sig.up_by_sample, pt, 'proteomics_up')
        _run(exp_data.proteins.sig.down_by_sample, pt, 'proteomics_down')

    if len(rt) != 0:
        _run(exp_data.rna.sig.by_sample, rt, 'rna_both')
        _run(exp_data.rna.sig.down_by_sample, rt, 'rna_down')
        _run(exp_data.rna.sig.up_by_sample, rt, 'rna_up')

    print("Done with enrichment")


def do_all(project_name, raptr_file):
    add_project_from_zip(project_name, raptr_file)
    add_enrichment(project_name)


if __name__ == '__main__':
    # new_proj = ['jak_atra', 'jak_only', 'atra_only']
    do_all('bendamustine',
           'export_Period 1 Challenge_magine_20170808-120713655.zip')

    # for i in new_proj:
    #     add_project(i)
    #     add_enrichment(i)
    #     load_project(i)
    #     dump_project(i)
