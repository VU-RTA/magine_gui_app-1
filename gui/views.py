import json
import gui.forms as forms
from .models import Data, EnrichmentOutput
from gui.network_functions import path_between, create_subgraph, neighbors

from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from gui.enrichment_functions.enrichr_helper import return_table, model_to_json, return_table_from_model


def index(request):
    projects = Data.objects.all()
    _data = {'projects': projects}
    return HttpResponse(
        get_template('welcome.html', using='jinja2').render(_data)
    )


def network_stats(request):
    return HttpResponse(
        get_template('network_stats.html', using='jinja2').render()
    )


def project_details(request, project_name):
    ex = Data.objects.get(project_name=project_name)
    meas = json.loads(ex.all_measured)
    uni = json.loads(ex.uni_measured)
    time = json.loads(ex.time)
    uni_sig = json.loads(ex.sig_uni)
    sig = json.loads(ex.sig_measured)
    content = {
        'data': ex,
        'time': time,
        'all_measured': meas,
        'uni_measured': uni,
        'sig_measured': sig,
        'sig_uni': uni_sig,
    }
    return render(request, 'project_details.html', content)


def project_enrichment(request, project_name):
    print('pk', project_name)

    ex = EnrichmentOutput.objects.filter(project_name=project_name).values()
    data = model_to_json(ex)

    # template = get_template('simple_table_view.html', using='jinja2')
    return render(request, 'simple_table_view.html', data)


# FORMS
def add_new_project(request):
    if request.method == "POST":
        form = forms.ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.set_exp_data(form.cleaned_data['file'])
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.project_name)
    else:
        form = forms.ProjectForm()
        return render(request, 'add_data.html', {'form': form})


def ontology_analysis_from_list(request):
    if request.method == "GET":
        form = forms.ListOfSpeciesOntology(request.GET)
        if form.is_valid():
            genes = form.cleaned_data['list_of_species'].split(',')
            names = []
            for i in genes:
                i = i.upper()
                i = i.replace(' ', '')
                names.append(i)
            ont = form.cleaned_data['ontology']
            data = return_table(genes, ont)

            template = get_template('simple_table_view.html', using='jinja2')
            return HttpResponse(template.render(data))
    else:
        form = forms.ListOfSpeciesOntology()
    return render(request, 'form_ontology_from_list.html', {'form': form})


def view_enrichment_from_model(request):
    if request.method == "GET":
        form = forms.EnrichmentDatasetForm(request.GET)
        if form.is_valid():
            project_name = form.cleaned_data['project_name']
            category = form.cleaned_data['category']
            dbs = form.cleaned_data['dbs']
            data = return_table_from_model(project_name, category,dbs)
            template = get_template('simple_table_view.html', using='jinja2')
            return HttpResponse(template.render(data))
    else:
        form = forms.EnrichmentDatasetForm()
    return render(request, 'form_ontology_from_list.html', {'form': form})


def generate_subgraph_from_list(request):
    if request.method == "GET":
        form = forms.ListOfSpeciesFrom(request.GET)
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
        form = forms.ListOfSpeciesFrom()
    return render(request, 'form_species_list.html', {'form': form})


def generate_path_between_two(request):
    if request.method == "GET":
        form = forms.PathBetweenForm(request.GET)
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
        form = forms.PathBetweenForm()
    return render(request, 'form_species_to_species.html', {'form': form})


def generate_neighbors(request):
    if request.method == "GET":
        form = forms.NodeNeighborsForm(request.GET)
        if form.is_valid():
            node = form.cleaned_data['node']
            start = node.upper()

            up_stream = form.cleaned_data['up_stream']
            down_stream = form.cleaned_data['down_stream']
            max_dist = int(form.cleaned_data['max_dist'])
            graph = neighbors(start, up_stream, down_stream, max_dist)
            data = {
                'nodes': json.dumps(graph['elements']['nodes']),
                'edges': json.dumps(graph['elements']['edges']),
            }

            template = get_template('subgraph_view.html', using='jinja2')
            return HttpResponse(template.render(data))
    else:
        form = forms.NodeNeighborsForm(initial={'max_dist': '1'})
    return render(request, 'form_graph_neighbors.html', {'form': form})
