from django.db import models
from django.utils import timezone
from magine.data.datatypes import ExperimentalData
from gui.data_functions import get_significant_numbers
import pandas as pd
import json
import os
# Create your models here.


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
