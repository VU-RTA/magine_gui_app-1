from django.conf.urls import url, include
from . import views


network_urls = [
    url(r'^subgraph$', views.SubgraphView.as_view(), name='subgraph'),
    url(r'^path$', views.ShortestPathView.as_view(), name='path'),
    url(r'^neighbors$', views.NeighorsView.as_view(), name='neighbors'),
    url(r'^network_stats$', views.network_stats, name='network_stats'),
]


enrichment_urls = [
    url(r'^filter$', views.ProjectEnrichmentView.as_view(), name='filter'),
    url(r'^enrichment$', views.EnrichmentResultsView.as_view(), name='enrichment'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.NewProjectView.as_view(), name='add'),

    url(r'^projects/(?P<project_name>[\w|\W]+)/',
        include([
            url(r'^details$', views.project_details, name='details'),
            url(r'^results$', views.project_enrichment, name='results'),
        ])
        ),



]
urlpatterns += network_urls + enrichment_urls
