from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index),
	url(r'^accounts/register$', views.register),
	url(r'^empresa/vaga/new$', views.new_vaga),
	url(r'^empresa/vaga/list$', views.list_vagas),
	url(r'^empresa/vaga/edit/(\d+)$', views.edit_vaga),
	url(r'^empresa/vaga/delete/(\d+)$', views.delete_vaga),
	url(r'^empresa/vaga/candidatos/(\d+)$', views.candidatos_vaga),
	url(r'^empresa/vaga/candidatos/changestatus/(\d+)$', views.change_status),
	url(r'^candidato/vagas$', views.candidato_vagas),
	url(r'^candidato/candidatarse/(\d+)/$', views.candidatarse),
	url(r'^candidato/candidaturas$', views.candidaturas),
	url(r'^candidato/candidaturas/delete/(\d+)$', views.delete_candidatura),
]