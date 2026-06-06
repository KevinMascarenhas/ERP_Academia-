from django.urls import path

from .api_views import PagamentoDetailApiView, PagamentoListCreateApiView
from .api_views import PagamentoAtrasarApiView, PagamentoPagarApiView

urlpatterns = [
    path("", PagamentoListCreateApiView.as_view(), name="api_pagamentos_list_create"),
    path("<int:id>/", PagamentoDetailApiView.as_view(), name="api_pagamentos_detail"),
    path("<int:id>/pagar/", PagamentoPagarApiView.as_view(), name="api_pagamentos_pagar"),
    path("<int:id>/atrasar/", PagamentoAtrasarApiView.as_view(), name="api_pagamentos_atrasar"),
]
