from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_planos, name="listar_planos"),
    path("criar/", views.criar_plano, name="criar_plano"),
    path("editar/<int:id_plano>/", views.editar_plano, name="editar_plano"),
    path("excluir/<int:id_plano>/", views.excluir_plano, name="excluir_plano"),
]
