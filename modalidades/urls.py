from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_modalidades, name="listar_modalidades"),
    path("criar/", views.criar_modalidade, name="criar_modalidade"),
    path("editar/<int:pk>/", views.editar_modalidade, name="editar_modalidade"),
    path("excluir/<int:pk>/", views.excluir_modalidade, name="excluir_modalidade"),
]
