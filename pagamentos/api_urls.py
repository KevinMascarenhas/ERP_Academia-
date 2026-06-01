from django.urls import path

from .api_views import PagamentoDetailApiView, PagamentoListCreateApiView

urlpatterns = [
    path("", PagamentoListCreateApiView.as_view(), name="api_pagamentos_list_create"),
    path("<int:id>/", PagamentoDetailApiView.as_view(), name="api_pagamentos_detail"),
]
