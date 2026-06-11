from django.urls import path
from . import views

urlpatterns = [
    # REST API endpoints (visíveis no Swagger)
    path("", views.modalidades_list_api, name="api_modalidades_list"),
    path("<int:pk>/", views.modalidades_detail_api, name="api_modalidades_detail"),
    path("inscricoes/", views.criar_inscricao_api, name="api_criar_inscricao"),
    path("inscricoes/<int:pk>/confirmar/", views.confirmar_inscricao_api, name="api_confirmar_inscricao"),
    path("inscricoes/<int:pk>/cancelar/", views.cancelar_inscricao_api, name="api_cancelar_inscricao"),
    path("frequencias/", views.frequencias_list_api, name="api_frequencias_list"),
    path("frequencias/<int:pk>/", views.frequencias_detail_api, name="api_frequencias_detail"),
    path("turmas/", views.turmas_list_api, name="api_turmas_list"),
    path("turmas/<int:turma_id>/inscricoes/", views.inscrever_aluno_turma_api, name="api_turma_inscricao"),
    path("turmas/inscricoes/<int:pk>/", views.cancelar_inscricao_turma_api, name="api_turma_inscricao_cancelar"),
    # HTML views (templates)
    path("lista/", views.listar_modalidades, name="listar_modalidades"),
    path("turmas/lista/", views.listar_turmas, name="listar_turmas"),
    path("registrar/<int:pk>/", views.registrar_modalidade, name="registrar_modalidade"),
    path("cancelar/<int:pk>/", views.cancelar_registro_modalidade, name="cancelar_registro_modalidade"),
    path("criar/", views.criar_modalidade, name="criar_modalidade"),
    path("editar/<int:pk>/", views.editar_modalidade, name="editar_modalidade"),
    path("excluir/<int:pk>/", views.excluir_modalidade, name="excluir_modalidade"),
    path("frequencias/lista/", views.listar_frequencias, name="listar_frequencias"),
    path("frequencias/criar/", views.criar_frequencia, name="criar_frequencia"),
    path("frequencias/editar/<int:pk>/", views.editar_frequencia, name="editar_frequencia"),
    path("frequencias/excluir/<int:pk>/", views.excluir_frequencia, name="excluir_frequencia"),
]
