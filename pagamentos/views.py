from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from academia.models import Aluno, Usuario
from academia.views import perfil_required

from .models import Pagamento


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_GET
def listar_pagamentos(request):
    pagamentos = Pagamento.objects.select_related("aluno").all()
    return render(request, "pagamentos/listar_pagamentos.html", {"usuario": request.user, "pagamentos": pagamentos})


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def criar_pagamento(request):
    if request.method == "POST":
        Pagamento.objects.create(
            aluno_id=request.POST.get("aluno_id"),
            valor=request.POST.get("valor"),
            mes_ano=request.POST.get("mes_ano"),
            status=request.POST.get("status"),
        )
        return redirect("listar_pagamentos")
    return render(
        request,
        "pagamentos/criar_pagamento.html",
        {"usuario": request.user, "alunos": Aluno.objects.order_by("nome"), "acao": "Criar"},
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_http_methods(["GET", "POST"])
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    if request.method == "POST":
        pagamento.aluno_id = request.POST.get("aluno_id")
        pagamento.valor = request.POST.get("valor")
        pagamento.mes_ano = request.POST.get("mes_ano")
        pagamento.status = request.POST.get("status")
        pagamento.save()
        return redirect("listar_pagamentos")
    return render(
        request,
        "pagamentos/editar_pagamento.html",
        {"usuario": request.user, "pagamento": pagamento, "alunos": Aluno.objects.order_by("nome"), "acao": "Editar"},
    )


@perfil_required(Usuario.PERFIL_ADMIN, Usuario.PERFIL_FUNCIONARIO)
@require_POST
def excluir_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    pagamento.delete()
    return redirect("listar_pagamentos")
