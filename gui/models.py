from django.db import models
from django.utils import timezone
from gui.data_functions import get_significant_numbers
import pandas as pd
import json



class Data(models.Model):
    project_name = models.CharField(max_length=200)
    upload_date = models.DateField(blank=True, null=True)
    #file_name_path = models.CharField(max_length=200, blank=True)
    stats = models.CharField(max_length=200, blank=True)
    times = models.CharField(max_length=200, blank=True)

    def publish(self):
        self.upload_date = timezone.now()

    def set_exp_data(self, file):
        df = pd.read_csv(file, low_memory=False)
        stats, times = get_significant_numbers(df, True, True)
        _times = [str(i) for i in times]
        self.stats = json.dumps(stats)
        self.times = json.dumps(_times)

    def get_stats(self):
        return json.loads(self.stats)

    def get_times(self):
        return json.loads(self.times)

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
    p_value_group_1_and_group_2 = models.FloatField()  # 'p_value_group_1_and_group_2'
    treated_control_fold_change = models.FloatField()  # 'treated_control_fold_change'
    significant_flag = models.BooleanField()  # 'significant_flag'
    exp_method = models.CharField(max_length=200)  # 'data_type'
    species_type = models.CharField(max_length=200)  # 'species_type'
    sample_id = models.CharField(max_length=200)  # 'time'
    data_type = models.CharField(max_length=100)


class Dataset(models.Model):
    project_name = models.CharField(max_length=200)
    measurements = models.ManyToManyField(Measurement)
