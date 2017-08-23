from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.add_new_project, name='add'),
    url(r'^projects/(?P<project_name>[\w|\W]+)/', include([
        url(r'^details$', views.project_details, name='details'),
        url(r'^results$', views.project_enrichment, name='results'),

    ])),
    url(r'^filter$', views.view_enrichment_from_model, name='filter'),
    # url(r'^(?P<project_name>[\w|\W]+)/results/', views.project_enrichment, name='results'),
    url(r'^subgraph$', views.generate_subgraph_from_list, name='subgraph'),
    url(r'^enrichment$', views.ontology_analysis_from_list, name='enrichment'),
    url(r'^path$', views.generate_path_between_two, name='path'),
    url(r'^neighbors$', views.generate_neighbors, name='neighbors'),
    url(r'^network_stats$', views.network_stats, name='network_stats'),
]
