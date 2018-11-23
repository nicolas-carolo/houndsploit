from django.conf.urls import include, url
from searcher import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
]