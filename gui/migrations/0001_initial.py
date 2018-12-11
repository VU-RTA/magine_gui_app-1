# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-11 18:48
from __future__ import unicode_literals

import picklefield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('upload_date', models.DateField(blank=True, null=True)),
                ('data', picklefield.fields.PickledObjectField(blank=True,
                                                               editable=False,
                                                               null=True)),
                ('time_points', models.CharField(blank=True, max_length=2000)),
                ('modality', models.CharField(blank=True, max_length=2000)),
                ('time', models.CharField(blank=True, max_length=2000)),
                ('all_measured',
                 models.CharField(blank=True, max_length=20000)),
                ('uni_measured',
                 models.CharField(blank=True, max_length=20000)),
                ('sig_measured',
                 models.CharField(blank=True, max_length=20000)),
                ('sig_uni', models.CharField(blank=True, max_length=20000)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EnrichmentOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(blank=True, max_length=200)),
                ('category', models.CharField(blank=True, max_length=200)),
                ('db', models.CharField(blank=True, max_length=200)),
                ('term_name', models.CharField(blank=True, max_length=20000)),
                ('term_id', models.CharField(blank=True, max_length=20000)),
                ('sample_id', models.CharField(blank=True, max_length=20000)),
                ('genes', models.CharField(blank=True, max_length=20000)),
                ('n_genes', models.IntegerField(blank=True, default=0)),
                ('rank', models.IntegerField(blank=True, default=0)),
                ('z_score', models.FloatField(blank=True, default=0)),
                ('p_value', models.FloatField(blank=True, default=0)),
                ('adj_p_value', models.FloatField(blank=True, default=0)),
                ('combined_score', models.FloatField(blank=True, default=0)),
                ('significant', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('fold_change', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='GeneList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('sample_id', models.CharField(blank=True, max_length=200)),
                ('gene_list', models.ManyToManyField(to='gui.Gene')),
            ],
            options={
                'ordering': ('sample_id',),
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('gene', models.CharField(blank=True, max_length=200)),
                ('protein', models.CharField(blank=True, max_length=200)),
                ('compound', models.CharField(blank=True, max_length=200)),
                ('compound_id', models.CharField(blank=True, max_length=200)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('p_value_group_1_and_group_2', models.FloatField()),
                ('treated_control_fold_change', models.FloatField()),
                ('significant_flag', models.BooleanField()),
                ('exp_method', models.CharField(max_length=200)),
                ('species_type', models.CharField(max_length=200)),
                ('sample_id', models.CharField(max_length=200)),
                ('data_type', models.CharField(max_length=100)),
                ('project_name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_name',
                 models.CharField(blank=True, max_length=200, primary_key=True,
                                  serialize=False, unique=True)),
                ('samples', models.ManyToManyField(to='gui.GeneList')),
            ],
        ),
        migrations.AddField(
            model_name='dataset',
            name='measurements',
            field=models.ManyToManyField(to='gui.Measurement'),
        ),
    ]