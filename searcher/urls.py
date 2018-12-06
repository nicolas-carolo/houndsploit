from django.conf.urls import url
from searcher import views

urlpatterns = [
    url(r'^$', views.get_results_table, name='get_results_table'),
    url(r'^view/(?P<id>\d+)/$', views.view_code, name='view_code'),
]