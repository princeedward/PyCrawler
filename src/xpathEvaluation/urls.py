from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='XpathIndex'),
    url(r'^eval/$', views.xeval, name='XpathEval'),
]
