from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_treinos, name="listar_treinos"),
    path("criar/", views.criar_treino, name="criar_treino"),
    path("editar/<int:id_treino>/", views.editar_treino, name="editar_treino"),
    path("excluir/<int:id_treino>/", views.excluir_treino, name="excluir_treino"),
]
