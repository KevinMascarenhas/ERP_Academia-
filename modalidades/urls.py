from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_modalidades, name="listar_modalidades"),
    path("registrar/<int:pk>/", views.registrar_modalidade, name="registrar_modalidade"),
    path("cancelar/<int:pk>/", views.cancelar_registro_modalidade, name="cancelar_registro_modalidade"),
    path("criar/", views.criar_modalidade, name="criar_modalidade"),
    path("editar/<int:pk>/", views.editar_modalidade, name="editar_modalidade"),
    path("excluir/<int:pk>/", views.excluir_modalidade, name="excluir_modalidade"),
    path("frequencias/", views.listar_frequencias, name="listar_frequencias"),
    path("frequencias/criar/", views.criar_frequencia, name="criar_frequencia"),
    path("frequencias/editar/<int:pk>/", views.editar_frequencia, name="editar_frequencia"),
    path("frequencias/excluir/<int:pk>/", views.excluir_frequencia, name="excluir_frequencia"),
]
