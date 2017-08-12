from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.template.loader import get_template
from gui.data_functions import get_significant_numbers
import pandas as pd
from django.core import serializers
from .forms import ProjectForm, ListOfSpeciesFrom, PathBetweenForm, \
    NodeNeighborsForm
from .models import Data, Measurement
from gui.network_functions import path_between, create_subgraph, neighbors
import json


def index(reqest):
    projects = Data.objects.all()
    _data = {'projects': projects}
    return HttpResponse(
        get_template('welcome.html', using='jinja2').render(_data)
    )


def network_stats(reqest):
    return HttpResponse(
        get_template('network_stats.html', using='jinja2').render()
    )


def post_detail(request, pk):
    ex = Data.objects.get(project_name=pk)
    return render(request, 'project_details.html', {'data': ex})


def post_table(request):
    ex = Data.objects.get(project_name='cisplatin_test')
    df = pd.read_csv(ex.file_name_path, low_memory=False)
    stats, times = get_significant_numbers(df, True, True)
    # print(times)

    # return template.render(table_info, request)
    template = get_template('table_stats.html', using='jinja2')
    return HttpResponse(template.render({
        'dict_list': stats,
        'time': times,
        'title': ex.project_name
    },
        request))


# FORMS
def add_new_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.set_exp_data(form.cleaned_data['file'])
            df = pd.read_json(post.all_data)
            print(df.head(10))
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.project_name)
    else:
        form = ProjectForm()
        return render(request, 'add_data.html', {'form': form})


def generate_subgraph_from_list(request):
    if request.method == "GET":
        form = ListOfSpeciesFrom(request.GET)
        if form.is_valid():
            post = form.cleaned_data['list_of_species'].split(',')
            names = []
            for i in post:
                i = i.upper()
                i = i.replace(' ', '')
                names.append(i)

            graph = create_subgraph(names)
            response = {
                'nodes': json.dumps(graph['elements']['nodes']),
                'edges': json.dumps(graph['elements']['edges']),
            }

            template = get_template('subgraph_view.html', using='jinja2')
            return HttpResponse(template.render(response))
    else:
        form = ListOfSpeciesFrom()
    return render(request, 'form_species_list.html', {'form': form})


def generate_path_between_two(request):
    if request.method == "GET":
        form = PathBetweenForm(request.GET)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            start = start.upper()
            end = end.upper()
            bi_dir = form.cleaned_data['bi_dir']
            graph = path_between(start, end, bi_dir)
            data = {
                'nodes': json.dumps(graph['elements']['nodes']),
                'edges': json.dumps(graph['elements']['edges']),
            }

            template = get_template('subgraph_view.html', using='jinja2')
            return HttpResponse(template.render(data))
    else:
        form = PathBetweenForm()
    return render(request, 'form_species_to_species.html', {'form': form})


def generate_neighbors(request):
    if request.method == "GET":
        form = NodeNeighborsForm(request.GET)
        if form.is_valid():
            node = form.cleaned_data['node']
            start = node.upper()

            up_stream = form.cleaned_data['up_stream']
            down_stream = form.cleaned_data['down_stream']
            graph = neighbors(start, up_stream, down_stream)
            data = {
                'nodes': json.dumps(graph['elements']['nodes']),
                'edges': json.dumps(graph['elements']['edges']),
            }

            template = get_template('subgraph_view.html', using='jinja2')
            return HttpResponse(template.render(data))
    else:
        form = NodeNeighborsForm()
    return render(request, 'form_graph_neighbors.html', {'form': form})


# AJAV views
def myModel_asJson(request):

    items = Measurement.objects.filter(project_name='Cisplatin')
    items = items.distinct()
    _valid_cols = ['gene', 'protein',
                   'p_value_group_1_and_group_2',
                   'treated_control_fold_change',
                   'significant_flag',
                   'data_type',
                   'sample_id']

    items = items.filter(significant_flag=True,
                         species_type='protein',
                         )

    items = list(items.values_list(*_valid_cols))
    formatted = []
    for i in items:
        tmp = list()
        tmp.append(i[0])
        tmp.append(i[1])
        tmp.append("{0:.2g}".format((i[2])))
        tmp.append("{0:.2f}".format((i[3])))
        tmp.append(i[4])
        tmp.append(i[5])
        tmp.append(i[6])
        formatted.append(tmp)
    items = json.dumps(dict(data=formatted))
    return HttpResponse(items, content_type='application/json')


def view_gene_table(request):
    # items = Measurement.objects.filter(project_name='Cisplatin')
    # print(len(items))
    # items = items.filter(significant_flag=True,
    #                      species_type='protein',
    #                      gene='BAX')
    # print(len(items))
    #
    # items = items.values()
    # print(len(items))
    # items = json.dumps(list(items))
    # context = {'items': mark_safe(items),}
    return render(request, 'list_genes.html')
    # return render(request, 'list_genes.html', {'items': items})
