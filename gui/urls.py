from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/new/$', views.add_new_project, name='add_new_project'),
    url(r'^post/(?P<pk>[\w|\W]+)/$', views.post_detail, name='post_detail'),
    url(r'^$', views.post_table, name='post_table'),
    url(r'^subgraph$', views.generate_subgraph_from_list, name='subgraph'),
    url(r'^path$', views.generate_path_between_two, name='path'),
    url(r'^neighbors$', views.generate_neighbors, name='neighbors'),
    url(r'^network_stats$', views.network_stats, name='network_stats'),
    # url(r'^data/$', views.display_data, name='data'),
]
