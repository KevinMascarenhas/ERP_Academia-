from django.urls import path
from . import views

urlpatterns = [
    path("", views.listar_pagamentos, name="listar_pagamentos"),
    path("criar/", views.criar_pagamento, name="criar_pagamento"),
    path("editar/<int:pagamento_id>/", views.editar_pagamento, name="editar_pagamento"),
    path("excluir/<int:pagamento_id>/", views.excluir_pagamento, name="excluir_pagamento"),
]
