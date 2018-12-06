from django.conf.urls import url
from searcher import views

urlpatterns = [
    url(r'^$', views.get_results_table, name='get_results_table'),
    url(r'^view/(?P<exploit_id>\d+)/$', views.view_exploit_code, name='view_code'),
]