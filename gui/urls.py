from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/new/$', views.add_new_project, name='add_new_project'),
    url(r'^post/(?P<pk>[\w|\W]+)/$', views.project_detail, name='post_detail'),
    url(r'^subgraph$', views.generate_subgraph_from_list, name='subgraph'),
    url(r'^enrichment$', views.ontology_analysis_from_list, name='enrichment'),
    url(r'^path$', views.generate_path_between_two, name='path'),
    url(r'^neighbors$', views.generate_neighbors, name='neighbors'),
    url(r'^network_stats$', views.network_stats, name='network_stats'),
    url(r'^measurements$', views.view_gene_table, name='measurements'),
    url(r'^measurements_ajax$', views.myModel_asJson, name='measurements_ajax'),
    # url(r'^data/$', views.display_data, name='data'),
]
