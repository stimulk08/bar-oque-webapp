CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'https://localhost:443',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://127.0.0.1:9000',
)
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'user-agent',
    'accept-encoding',
    'user-timezone'
)
CORS_ALLOW_CREDENTIALS = True
