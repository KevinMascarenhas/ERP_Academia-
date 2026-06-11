from django.urls import path
from . import views

urlpatterns = [
    # REST API endpoints (visíveis no Swagger)
    path("", views.treinos_list_api, name="api_treinos_list"),
    path("<int:id_treino>/", views.treinos_detail_api, name="api_treinos_detail"),
    # HTML views (templates)
    path("lista/", views.listar_treinos, name="listar_treinos"),
    path("sugestoes/", views.sugerir_treino, name="sugerir_treino"),
    path("criar/", views.criar_treino, name="criar_treino"),
    path("editar/<int:id_treino>/", views.editar_treino, name="editar_treino"),
    path("excluir/<int:id_treino>/", views.excluir_treino, name="excluir_treino"),
]

