from django.urls import path

from .api_views import (
    InscricaoCancelarApiView,
    InscricaoConfirmarApiView,
    FrequenciaDetailApiView,
    FrequenciaListCreateApiView,
    InscricaoDetailApiView,
    InscricaoListCreateApiView,
    ModalidadeDetailApiView,
    ModalidadeListCreateApiView,
)

urlpatterns = [
    path("", ModalidadeListCreateApiView.as_view(), name="api_modalidades_list_create"),
    path("<int:id>/", ModalidadeDetailApiView.as_view(), name="api_modalidades_detail"),
    path("inscricoes/", InscricaoListCreateApiView.as_view(), name="api_inscricoes_list_create"),
    path("inscricoes/<int:id>/", InscricaoDetailApiView.as_view(), name="api_inscricoes_detail"),
    path("inscricoes/<int:id>/confirmar/", InscricaoConfirmarApiView.as_view(), name="api_inscricoes_confirmar"),
    path("inscricoes/<int:id>/cancelar/", InscricaoCancelarApiView.as_view(), name="api_inscricoes_cancelar"),
    path("frequencias/", FrequenciaListCreateApiView.as_view(), name="api_frequencias_list_create"),
    path("frequencias/<int:id>/", FrequenciaDetailApiView.as_view(), name="api_frequencias_detail"),
]
