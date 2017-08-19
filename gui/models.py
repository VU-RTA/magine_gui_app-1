from django.db import models
from django.utils import timezone
from gui.data_functions import get_all_tables
import pandas as pd
from picklefield.fields import PickledObjectField
import json
from magine_gui_app.settings import BASE_DIR
import os

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

    def set_exp_data(self, file):
        data = pd.read_csv(file, low_memory=False)
        self.time_points = ','.join(list(data['time'].astype(str).unique()))
        self.modality = ','.join(list(data['data_type'].unique()))
        time, all_m, uni_m, sig_m, sig_uni = get_all_tables(data)
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

    def _str__(self):
        return self.project_name


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
    p_value_group_1_and_group_2 = models.FloatField()  # 'p_value_group_1_and_group_2'
    treated_control_fold_change = models.FloatField()  # 'treated_control_fold_change'
    significant_flag = models.BooleanField()  # 'significant_flag'
    exp_method = models.CharField(max_length=200)  # 'data_type'
    species_type = models.CharField(max_length=200)  # 'species_type'
    sample_id = models.CharField(max_length=200)  # 'time'
    data_type = models.CharField(max_length=100)
    project_name = models.CharField(max_length=200, blank=True)


class Dataset(models.Model):
    project_name = models.CharField(max_length=200)
    measurements = models.ManyToManyField(Measurement)


class EnrichmentOutput(models.Model):
    project_name = models.CharField(max_length=200, blank=True)
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



