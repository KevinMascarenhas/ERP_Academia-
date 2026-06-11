from django.urls import path
from . import views

urlpatterns = [
    # REST API endpoints (visíveis no Swagger)
    path("", views.planos_list_api, name="api_planos_list"),
    path("<int:id_plano>/", views.planos_detail_api, name="api_planos_detail"),
    # HTML views (templates)
    path("lista/", views.listar_planos, name="listar_planos"),
    path("meu/", views.meu_plano, name="meu_plano"),
    path("criar/", views.criar_plano, name="criar_plano"),
    path("editar/<int:id_plano>/", views.editar_plano, name="editar_plano"),
    path("excluir/<int:id_plano>/", views.excluir_plano, name="excluir_plano"),
]

