from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from functools import wraps

# Decorators de controle de acesso
def perfil_required(*perfis):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.perfil not in perfis:
                return render(request, "acesso_negado.html")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Tela de Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("password", "")
        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"erro": "Email ou senha invalidos.", "email": email},
        )

    return render(request, "login.html")


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def dashboard_view(request):
    perfil = request.user.perfil
    if perfil == "Administrador":
        return render(request, "dashboard_admin.html")
    elif perfil == "Funcionário":
        return render(request, "dashboard_funcionario.html")
    elif perfil == "Aluno":
        return render(request, "dashboard_aluno.html")
    return redirect("login")

def acesso_negado_view(request):
    return render(request, "acesso_negado.html")

@perfil_required("Administrador")
def dashboard_admin_view(request):
    return render(request, "dashboard_admin.html", {"usuario": request.user})

@perfil_required("Funcionário")
def dashboard_funcionario_view(request):
    return render(request, "dashboard_funcionario.html", {"usuario": request.user})

@perfil_required("Aluno")
def dashboard_aluno_view(request):
    return render(request, "dashboard_aluno.html", {"usuario": request.user})
