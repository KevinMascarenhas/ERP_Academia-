from django.urls import path
from . import views

urlpatterns = [
    # REST API endpoints (visíveis no Swagger)
    path("", views.pagamentos_list_api, name="api_pagamentos_list"),
    path("<int:pagamento_id>/", views.pagamentos_detail_api, name="api_pagamentos_detail"),
    # HTML views (templates)
    path("lista/", views.listar_pagamentos, name="listar_pagamentos"),
    path("criar/", views.criar_pagamento, name="criar_pagamento"),
    path("editar/<int:pagamento_id>/", views.editar_pagamento, name="editar_pagamento"),
    path("excluir/<int:pagamento_id>/", views.excluir_pagamento, name="excluir_pagamento"),
]
