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


def add_project(proj_name):
    print('saving {}'.format(proj_name))
    there = Data.objects.all().filter(project_name=proj_name)
    if len(there) > 0:
        there.delete()

    new = Data.objects.create(project_name=proj_name)
    new.set_exp_data(
        os.path.join(os.path.dirname(__file__), '{}.csv.gz'.format(proj_name)),
        set_time_point=True,
    )
    new.save()
    print(new.get_time_points())
    print('saved')


def dump_project(proj_name):
    there = EnrichmentOutput.objects.all().filter(project_name=proj_name)
    df = pd.DataFrame(list(there.values()))
    print(df.dtypes)
    print(df['sample_id'].unique())
    df = df[df['sample_id'].isin(['01hr', '24hr', '06hr', '48hr', '72hr', '96hr'])]
    print(df['sample_id'].unique())
    df.to_csv('{}_enrichment_dump.csv.gz'.format(proj_name), compression='gzip')


def add_enrichment(project_name):

    already_there = set()
    for i in EnrichmentOutput.objects.all():
        already_there.add((str(i.db), str(i.category), str(i.sample_id).replace(' ', ''), project_name))

    all_dbs = [

        'KEGG_2016',
        'NCI-Nature_2016',
        'Panther_2016',
        'WikiPathways_2016',
        'BioCarta_2016',
        'Humancyc_2016',
        'Reactome_2016',
        'KEA_2015',

        # ontologies
        'GO_Biological_Process_2017',
        'GO_Molecular_Function_2017',
        'GO_Cellular_Component_2017',

        # transcription
        'ChEA_2016',
        'TRANSFAC_and_JASPAR_PWMs',
        'ENCODE_TF_ChIP-seq_2015',


        # cell types
        'Jensen_TISSUES',
        'Human_Gene_Atlas',
        'Tissue_Protein_Expression_from_ProteomicsDB',
        'ARCHS4_Cell-lines',
        'ARCHS4_Tissues',
        'Cancer_Cell_Line_Encyclopedia',
        'NCI-60_Cancer_Cell_Lines',

        # pertubations
        'Kinase_Perturbations_from_GEO_down',
        'Kinase_Perturbations_from_GEO_up',
        'LINCS_L1000_Kinase_Perturbations_down',
        'LINCS_L1000_Kinase_Perturbations_up',
        'Old_CMAP_down',
        'Old_CMAP_up',

        # phenotypes
        'Human_Phenotype_Ontology',
        'MGI_Mammalian_Phenotype_2017',
        'Jensen_DISEASES',
        'dbGaP',
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
                if current in already_there:
                    continue
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
    _run(exp.proteomics_over_time, pt, 'proteomics_both')
    _run(exp.proteomics_down_over_time, pt, 'proteomics_down')
    _run(exp.proteomics_up_over_time, pt, 'proteomics_up')
    _run(exp.rna_down_over_time, rt, 'rna_down')
    _run(exp.rna_up_over_time, rt, 'rna_up')
    _run(exp.rna_over_time, rt, 'rna_both')
    #
    print("Done with enrichment")


if __name__ == '__main__':
    # add_meth()
    # add_cisplatin()
    # dump_project('incyte_jak_atra')
    # add_project('incyte_jak_atra')
    add_enrichment('incyte_jak_atra')
    # add_enrichment('cisplatin')
    #
    # add_bend()
    # add_enrichment('bendamustine')
