from django.urls import path

from .api_views import SugestaoTreinoApiView, TreinoDetailApiView, TreinoListCreateApiView

urlpatterns = [
    path("", TreinoListCreateApiView.as_view(), name="api_treinos_list_create"),
    path("sugerir/", SugestaoTreinoApiView.as_view(), name="api_treinos_sugerir"),
    path("<int:id_treino>/", TreinoDetailApiView.as_view(), name="api_treinos_detail"),
]
