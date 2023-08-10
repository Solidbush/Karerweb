from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication

User = get_user_model()


class BasicAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        username_password = header.decode().split(' ')
        if not len(username_password) == 2:
            return None
        username_password = username_password[1].split(':')
        try:
            user = User.objects.get(email=username_password[0])
            user.check_password(username_password[1])
            return user, True
        except (User.DoesNotExist, ValueError):
            raise AuthenticationFailed(_("Token contained no recognizable user identification"))
