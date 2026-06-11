from django.contrib import admin
from django.contrib.staticfiles.views import serve as static_serve
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/academia/", include("academia.urls")),
    path("api/planos/", include("planos.urls")),
    path("api/modalidades/", include("modalidades.urls")),
    path("api/treinos/", include("treinos.urls")),
    path("api/pagamentos/", include("pagamentos.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Development-only static file serving so /static/* works even when DEBUG=False locally.
    path("static/<path:path>", static_serve),
]
