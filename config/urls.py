from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("admin/", admin.site.urls),
    path("academia/", include("academia.urls")),
    path("modalidades/", include("modalidades.urls")),
    path("planos/", include("planos.urls")),
    path("treinos/", include("treinos.urls")),
    path("pagamentos/", include("pagamentos.urls")),
    path("api/academia/", include("academia.api_urls")),
    path("api/planos/", include("planos.api_urls")),
    path("api/modalidades/", include("modalidades.api_urls")),
    path("api/treinos/", include("treinos.api_urls")),
    path("api/pagamentos/", include("pagamentos.api_urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/", include("rest_framework.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
