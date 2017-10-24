import pandas as pd
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magine_gui_app.settings')
import sys
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from gui.models import Data, EnrichmentOutput
from magine.ontology.enrichr import Enrichr
from magine.data.datatypes import ExperimentalData


from magine_gui_app.settings import BASE_DIR
_dir = BASE_DIR


def add_meth():
    print('saving methotrexate')
    there = Data.objects.all().filter(project_name='methotrexate')

    if len(there) > 0:
        there.delete()

    new = Data.objects.create(project_name='methotrexate')
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__), 'data.csv.gz'),
        set_time_point=True,
    )
    new.save()
    print(new.get_time_points())
    print('saved')


def add_bend():
    print('saving bendamustine')
    there = Data.objects.all().filter(project_name='bendamustine')
    if len(there) > 0:
        there.delete()

    new = Data.objects.create(project_name='bendamustine')
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__), 'bendamustine.csv.gz'),
        set_time_point=True,
    )
    new.save()
    print(new.get_time_points())
    print('saved')


def add_enrichment(project_name):

    already_there = set()
    for i in EnrichmentOutput.objects.all():
        already_there.add((str(i.db), str(i.category), str(i.sample_id).replace(' ', '')))

    all_dbs = [
        'GO_Biological_Process_2017',
        'GO_Molecular_Function_2017',
        'GO_Cellular_Component_2017',
        'KEGG_2016',
        'NCI-Nature_2016',
        'Panther_2016',
        'WikiPathways_2016',
        'BioCarta_2016',
        'Humancyc_2016',
        'Reactome_2016',
        'KEA_2015',
        'ChEA_2016',
        'DrugMatrix',
        'Drug_Perturbations_from_GEO_2014',
    ]
    e = Enrichr()
    d = Data.objects.all()
    data = d.filter(project_name=project_name)[0]
    exp = ExperimentalData(data.data)

    def _run(samples, timepoints, category):
        for genes, sample_id in zip(samples, timepoints):
            print("On sample {} of {}".format(sample_id, timepoints))
            for i in all_dbs:
                current = (str(i), str(category), str(sample_id), project_name)
                # x = EnrichmentOutput.objects.filter(db=i, category=category, sample_id=sample_id)
                # x.delete()
                print(current)

                name = os.path.join(_dir, 'test_data', 'CSVs',
                                    '_'.join(current) + '.csv.gz')
                try:
                    df = pd.read_csv(name, index_col=None, encoding='utf-8')
                except:
                    print("Need to fix {}".format(name))
                    # continue
                    df = e.run(genes, i)
                    df.to_csv(name, index=False, encoding='utf-8', compression='gzip')
                df['db'] = i
                df['sample_id'] = sample_id
                df['category'] = category
                df['project_name'] = project_name
                dict_list = df.to_dict(orient='records')
                # """
                list_to_save = []
                for row in dict_list:
                    m = EnrichmentOutput(**row)
                    list_to_save.append(m)

                EnrichmentOutput.objects.bulk_create(list_to_save)
                # """
    pt = exp.proteomics_time_points
    rt = exp.rna_time_points
    print(rt)
    print(exp.rna_up_over_time)
    # _run(exp.proteomics_over_time, pt, 'proteomics_both')
    # _run(exp.proteomics_down_over_time, pt, 'proteomics_down')
    # _run(exp.proteomics_up_over_time, pt, 'proteomics_up')
    _run(exp.rna_down_over_time, rt, 'rna_down')
    _run(exp.rna_up_over_time, rt, 'rna_up')
    _run(exp.rna_over_time, rt, 'rna_both')
    #
    print("Done with enrichment")


if __name__ == '__main__':
    add_meth()
    #
    # add_bend()
    # add_enrichment('bendamustine')
