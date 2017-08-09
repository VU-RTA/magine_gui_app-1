from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from gui.data_functions import get_significant_numbers
import pandas as pd
from .forms import ProjectForm, ListOfSpeciesFrom, PathBetweenForm
from .models import Data
from gui.network_functions import path_between, create_subgraph
import json


def index(reqest):
    projects = Data.objects.all()
    _data = {'projects': projects}
    return HttpResponse(
        get_template('welcome.html', using='jinja2').render(_data)
    )


def post_detail(request, pk):
    print(pk)
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
        print(form)
        print(form.is_valid())
        # print(form.cleaned_data['start'])
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            start = start.upper()
            end = end.upper()
            bi_dir = form.cleaned_data['bi_dir']
            print(bi_dir)
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


# def display_data(request):
#     ex = Data.objects.get(project_name='cisplatin_test')
#     df = pd.read_csv(ex.file_name_path, low_memory=False)
#     df = pivot_raw_gene_data(df)
#     table_info = process_filter_table(df, title=ex.project_name)
#     return render(request, 'filter_table.html', table_info)

"""
def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "import.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("myapp:upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("myapp:upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["name"] = fields[0]
            data_dict["start_date_time"] = fields[1]
            data_dict["end_date_time"] = fields[2]
            data_dict["notes"] = fields[3]
            try:
                form = EventsForm(data_dict)
                if form.is_valid():
                    form.save()
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())
            except Exception as e:
                logging.getLogger("error_logger").error(form.errors.as_json())
                pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("myapp:upload_csv"))
"""
