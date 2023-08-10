from .celery import app as celery_app
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from drf_spectacular.plumbing import build_bearer_security_scheme_object


__all__ = ['celery_app']


class BasicAuthScheme(SimpleJWTScheme):
    name = 'basicAuth'
    target_class = 'core.authentication.BasicAuthentication'

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='HTTP_AUTHORIZATION',
            token_prefix='Basic',
        )
