import json
import os

import pandas as pd
from django.db import models
from django.utils import timezone
from picklefield.fields import PickledObjectField

from gui.data_functions import get_all_tables
from magine.data.experimental_data import ExperimentalData, load_data_csv
from magine_gui_app.settings import BASE_DIR

data_dir = os.path.join(BASE_DIR, '_state')


class Data(models.Model):
    project_name = models.CharField(max_length=200)
    upload_date = models.DateField(blank=True, null=True)
    data = PickledObjectField(compress=True, blank=True)
    time_points = models.CharField(max_length=2000, blank=True)
    modality = models.CharField(max_length=2000, blank=True)
    time = models.CharField(max_length=2000, blank=True)
    all_measured = models.CharField(max_length=20000, blank=True)
    uni_measured = models.CharField(max_length=20000, blank=True)
    sig_measured = models.CharField(max_length=20000, blank=True)
    sig_uni = models.CharField(max_length=20000, blank=True)

    def publish(self):
        self.upload_date = timezone.now()

    def set_exp_data(self, file, set_time_point=False):
        if isinstance(file, pd.DataFrame):
            exp_data = ExperimentalData(file)
            data = ExperimentalData(file).data
        else:
            data = load_data_csv(file, low_memory=False)

        if set_time_point:
            data['time'] = data['sample_id']
        self.time_points = ','.join(
            sorted((data['sample_id'].astype(str).unique())))
        self.modality = ','.join(list(data['source'].unique()))

        time, all_m, uni_m, sig_m, sig_uni = get_all_tables(exp_data)
        self.time = json.dumps(time)
        self.all_measured = json.dumps(all_m)
        self.uni_measured = json.dumps(uni_m)
        self.sig_measured = json.dumps(sig_m)
        self.sig_uni = json.dumps(sig_uni)
        self.data = data
        self.save()

    def get_time_points(self):
        return self.time_points.split(',')

    def get_all_measured(self):
        return json.loads(self.all_measured)

    def get_modalities(self):
        return self.modality.split(',')

    def return_magine_data(self, project_name):
        data = self.objects.filter(project_name=project_name)[0]
        return ExperimentalData(data.data)

    def _str__(self):
        return self.project_name


class EnrichmentOutput(models.Model):
    project_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=200, blank=True)
    db = models.CharField(max_length=200, blank=True)

    term_name = models.CharField(max_length=20000, blank=True)
    term_id = models.CharField(max_length=20000, blank=True)
    sample_id = models.CharField(max_length=20000, blank=True)
    genes = models.CharField(max_length=20000, blank=True)

    n_genes = models.IntegerField(blank=True, default=0)
    rank = models.IntegerField(blank=True, default=0)

    z_score = models.FloatField(blank=True, default=0)
    p_value = models.FloatField(blank=True, default=0)
    adj_p_value = models.FloatField(blank=True, default=0)
    combined_score = models.FloatField(blank=True, default=0)
    significant = models.BooleanField(blank=True)


class Measurement(models.Model):
    DATA_TYPE = (
        'metabolite',
        'protein',
        'rna'
    )

    gene = models.CharField(max_length=200, blank=True)
    protein = models.CharField(max_length=200, blank=True)
    compound = models.CharField(max_length=200, blank=True)
    compound_id = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)
    p_value_group_1_and_group_2 = models.FloatField()
    treated_control_fold_change = models.FloatField()
    significant_flag = models.BooleanField()
    exp_method = models.CharField(max_length=200)
    species_type = models.CharField(max_length=200)
    sample_id = models.CharField(max_length=200)
    data_type = models.CharField(max_length=100)
    project_name = models.CharField(max_length=200, blank=True)


class Dataset(models.Model):
    project_name = models.CharField(max_length=200)
    measurements = models.ManyToManyField(Measurement)


class Gene(models.Model):
    name = models.CharField(max_length=200, blank=True)
    fold_change = models.IntegerField(blank=True, default=0)


class GeneList(models.Model):
    gene_list = models.ManyToManyField(Gene)
    sample_id = models.CharField(max_length=200, blank=True)

    def up_genes(self):
        return [i[0] for i in
                self.gene_list.filter(fold_change__gt=0).values_list('name')]

    def down_genes(self):
        return [i[0] for i in
                self.gene_list.filter(fold_change__lt=0).values_list('name')]

    class Meta:
        ordering = ('sample_id',)


class Project(models.Model):
    project_name = models.CharField(max_length=200, blank=True, unique=True,
                                    primary_key=True)

    samples = models.ManyToManyField(GeneList)
