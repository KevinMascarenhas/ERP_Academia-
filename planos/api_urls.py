from django.urls import path

from .api_views import PlanoDetailApiView, PlanoListCreateApiView

urlpatterns = [
    path("", PlanoListCreateApiView.as_view(), name="api_planos_list_create"),
    path("<int:id_plano>/", PlanoDetailApiView.as_view(), name="api_planos_detail"),
]
