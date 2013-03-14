from os import urandom

CSRF_ENABLED = True
SECURE_KEY = urandom(24)
