from rest_framework.permissions import BasePermission

from .models import Usuario


class IsAdminProfile(BasePermission):
    message = "Apenas administradores podem acessar este recurso."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.perfil == Usuario.PERFIL_ADMIN)


class IsAdminOrFuncionarioProfile(BasePermission):
    message = "Apenas administradores e funcionários podem acessar este recurso."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.perfil in {Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO}
        )
