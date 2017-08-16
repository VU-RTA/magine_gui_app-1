from django.db import models
from django.utils import timezone
from gui.data_functions import get_significant_numbers
import pandas as pd
from picklefield.fields import PickledObjectField
from magine_gui_app.settings import BASE_DIR
import os

data_dir = os.path.join(BASE_DIR, '_state')


class Data(models.Model):
    project_name = models.CharField(max_length=200)
    upload_date = models.DateField(blank=True, null=True)
    data = PickledObjectField(compress=True, blank=True)
    #file_name_path = models.CharField(max_length=200, blank=True)
    # stats = models.CharField(max_length=200, blank=True)
    # times = models.CharField(max_length=200, blank=True)
    # all_data = models.CharField(max_length=2000000, blank=True)

    def publish(self):
        self.upload_date = timezone.now()

    def set_exp_data(self, file):
        self.data = pd.read_csv(file, low_memory=False)
        self.save()

        # file_location = os.path.join(data_dir, self.project_name + '.csv.gz')

        # df.to_csv(file_location, compression='gzip')
        # stats, times = get_significant_numbers(df, True, True)
        # _times = [str(i) for i in times]
        # self.stats = json.dumps(stats)
        # self.times = json.dumps(_times)
        # self.all_data = df.to_json()

    def all_measurements(self):
        # file_location = os.path.join(data_dir, self.project_name + '.csv.gz')
        # df = pd.read_csv(file_location)
        data = self.data.copy()
        time, all_measured = get_significant_numbers(data, unique=False, sig=False)
        time, uni_measured = get_significant_numbers(data, unique=True, sig=False)
        time, sig_measured = get_significant_numbers(data, unique=False, sig=True)
        time, sig_uni = get_significant_numbers(data, unique=True, sig=True)
        return time, all_measured, uni_measured, sig_measured, sig_uni


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
