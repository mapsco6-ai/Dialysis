from .base import *  # noqa: F401,F403
from .base import env

DEBUG = False
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# No insecure fallback in production: fail loudly at startup rather than
# silently running with the dev placeholder secret key.
SECRET_KEY = env("DJANGO_SECRET_KEY")

# nginx terminates TLS and forwards plain HTTP internally, setting
# X-Forwarded-Proto - this tells Django to trust that header instead of
# looking at the (always-HTTP) connection it actually receives.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=31536000)
