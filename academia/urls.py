from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("dashboard/admin/", views.dashboard_admin_view, name="dashboard_admin"),
    path("dashboard/funcionario/", views.dashboard_funcionario_view, name="dashboard_funcionario"),
    path("dashboard/aluno/", views.dashboard_aluno_view, name="dashboard_aluno"),
    path("usuarios/", views.listar_usuarios, name="listar_usuarios"),
    path("usuarios/criar/", views.criar_usuario_view, name="criar_usuario"),
    path("usuarios/editar/<int:user_id>/", views.editar_usuario_view, name="editar_usuario"),
    path("usuarios/excluir/<int:user_id>/", views.excluir_usuario_view, name="excluir_usuario"),
    path("logout/", views.logout_view, name="logout"),
]
