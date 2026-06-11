from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class JWTCookieAuthentication(JWTAuthentication):
    """
    Autenticador que tenta ler o token JWT do cookie 'access_token'.
    Se não encontrado no cookie, delega ao comportamento padrão (header Authorization).
    Isso permite que o login pela tela HTML (que seta o cookie) funcione
    diretamente nas views DRF sem exigir o header Authorization.
    """

    def authenticate(self, request):
        # Tenta obter o token do cookie primeiro
        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            # Sem cookie: tenta o header Authorization padrão (Bearer token)
            return super().authenticate(request)

        try:
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            return user, validated_token
        except (InvalidToken, TokenError):
            # Token inválido/expirado no cookie — ignora e deixa falhar
            return None
