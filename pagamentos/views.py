from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from academia.views import perfil_required
from .models import Pagamento

@perfil_required("Administrador", "Funcionário")
@require_GET
def listar_pagamentos(request):
    pagamentos = Pagamento.objects.all()
    return render(request, "pagamentos/listar_pagamentos.html", {"pagamentos": pagamentos})

@perfil_required("Administrador", "Funcionário")
@require_http_methods(["GET", "POST"])
def criar_pagamento(request):
    if request.method == "POST":
        Pagamento.objects.create(
            aluno_id = request.POST.get("aluno_id"),
            valor = request.POST.get("valor"),
            mes_ano = request.POST.get("mes_ano"),
            status = request.POST.get("status")
        )
        return redirect("listar_pagamentos")
    return render(request, "pagamentos/criar_pagamento.html", {"pagamentos": Pagamento.objects.all(), "acao": "Criar"})

@perfil_required("Administrador", "Funcionário")
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
    return render(request, "pagamentos/editar_pagamento.html", {"pagamento": pagamento, "acao": "Editar"})

@perfil_required("Administrador", "Funcionário")
@require_POST
def excluir_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    if request.method == "POST":
        pagamento.delete()
        return redirect("listar_pagamentos")
    return render(request, "pagamentos/excluir_pagamento.html", {"pagamento": pagamento})
