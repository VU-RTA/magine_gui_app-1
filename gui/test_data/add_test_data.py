import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magine_gui_app.settings')
from django.core.wsgi import get_wsgi_application
get_wsgi_application()
from gui.models import Data, EnrichmentOutput


def add_meth():
    print('saving methotrexate')
    there = Data.objects.all()
    there.filter(project_name='methotrexate')
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


def add_enrichment():
    from magine.ontology.enrichr import Enrichr
    from magine.data.datatypes import ExperimentalData
    already_there = set()
    for i in EnrichmentOutput.objects.all():
        print(i.db, i.category, i.sample_id)
        already_there.add((i.db, i.category, i.sample_id))

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
    meth = d.filter(project_name='methotrexate')[0]
    exp = ExperimentalData(meth.data)

    def _run(samples, timepoints, category):
        for genes, sample_id in zip(samples, timepoints):
            print("On sample {} of {}".format(sample_id, timepoints))
            for i in all_dbs:
                current = (str(i), str(category),str(sample_id))
                if not current in already_there:
                    df = e.run(genes, i)
                    df['db'] = i
                    df['sample_id'] = sample_id
                    dict_list = df.to_dict(orient='records')
                    for i in dict_list:
                        m = EnrichmentOutput.objects.create(
                            project_name='methotrexate',
                            sample_id=sample_id,
                            category=category,
                            **i)
                        m.save()

            # df = e.run_set_of_dbs(genes, db='all')
            # dict_list = df.to_dict(orient='records')
            # for i in dict_list:
            #     m = EnrichmentOutput.objects.create(
            #         project_name='methotrexate',
            #         sample_id=sample_id,
            #         category=category,
            #         **i)
            #     m.save()
            return
    pt = exp.proteomics_time_points
    _run(exp.proteomics_down_over_time, pt, 'proteomics_down')

    _run(exp.proteomics_up_over_time, pt, 'proteomics_up')
    _run(exp.proteomics_over_time, pt, 'proteomics_both')

    # rt = exp.rna_time_points
    # _run(exp.rna_down_over_time, rt, 'rna_down')
    # _run(exp.rna_up_over_time, rt, 'rna_up')
    # _run(exp.rna_over_time, rt, 'rna_both')

    print("Done with enrichment")


if __name__ == '__main__':
    # add_meth()
    add_enrichment()
