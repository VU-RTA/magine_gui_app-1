from magine.enrichment.enrichr import Enrichr, db_types

# from celery import Celery
# app = Celery('tasks', broker='pyamqp://guest@localhost//')



# @app.task
def run(samples, sample_ids, label, p_name, already_there, EnrichmentOutput):
    standard_dbs = []
    dbs = ['drug', 'disease', 'ontologies', 'pathways', 'transcription',
           'kinases', 'histone', 'cell_type']
    for i in ['pathways']:
        standard_dbs += db_types[i]

    for genes, sample_id in zip(samples, sample_ids):
        print("Starting {}".format(sample_id))

        current = "{}_{}_{}".format(label, sample_id, p_name)

        if current not in already_there:
            e = Enrichr()
            df = e.run(genes, standard_dbs)
            if df.shape[0] == 0:
                print("No results found")
                continue
            df['significant'] = False
            crit = (df['adj_p_value'] <= 0.05) & (df['combined_score'] > 0)
            df.loc[crit, 'significant'] = True

            df['sample_id'] = sample_id
            df['category'] = label
            df['project_name'] = p_name
            EnrichmentOutput.objects.bulk_create(
                [EnrichmentOutput(**r) for r in df.to_dict(orient='records')]
            )

        print("Finished {}".format(sample_id))