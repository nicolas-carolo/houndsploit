from django.conf.urls import url
from searcher import views

urlpatterns = [
    url(r'^$', views.get_results_table, name='get_results_table'),
    url(r'^exploit_view/(?P<exploit_id>\d+)', views.view_exploit_code, name='view_exploit_code'),
    url(r'^shellcode_view/(?P<shellcode_id>\d+)', views.view_shellcode_code, name='view_shellcode_code'),
    url(r'^settings/', views.show_settings, name='show_settings'),
    url(r'^about/', views.show_info, name='show_info'),
    url(r'^advanced/$', views.get_results_table_advanced, name='get_results_table_advanced'),
    url(r'^suggested/(?P<suggested_input>[^/]*)', views.suggested_search, name='suggested_search'),
    url(r'^suggested_advanced/(?P<suggested_input>[^/]*)/(?P<operator_index>\d)/(?P<type_index>\d+)/'
        r'(?P<platform_index>\d+)/(?P<author>.+)/(?P<port>(\d+|None))/(?P<start_date>[^/]*)/(?P<end_date>[^/]*)',
        views.suggested_search_advanced, name='suggested_search_advanced'),
    url(r'^manage_suggestions/', views.show_suggestions, name='show_suggestions'),
    url(r'^add_suggestion/', views.add_suggestion, name='add_suggestion'),
    url(r'^delete_suggestion/(?P<suggestion_id>\d+)', views.delete_suggestion, name='delete_suggestion')

]
