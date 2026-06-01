from django.urls import path

from .api_views import (
    AdministradorDetailApiView,
    AdministradorListCreateApiView,
    AlunoDetailApiView,
    AlunoListCreateApiView,
    FuncionarioDetailApiView,
    FuncionarioListCreateApiView,
    UsuarioDetailApiView,
    UsuarioListCreateApiView,
)

urlpatterns = [
    path("usuarios/", UsuarioListCreateApiView.as_view(), name="api_usuarios_list_create"),
    path("usuarios/<int:id>/", UsuarioDetailApiView.as_view(), name="api_usuarios_detail"),
    path("administradores/", AdministradorListCreateApiView.as_view(), name="api_administradores_list_create"),
    path("administradores/<int:id>/", AdministradorDetailApiView.as_view(), name="api_administradores_detail"),
    path("funcionarios/", FuncionarioListCreateApiView.as_view(), name="api_funcionarios_list_create"),
    path("funcionarios/<int:id>/", FuncionarioDetailApiView.as_view(), name="api_funcionarios_detail"),
    path("alunos/", AlunoListCreateApiView.as_view(), name="api_alunos_list_create"),
    path("alunos/<int:id>/", AlunoDetailApiView.as_view(), name="api_alunos_detail"),
]
