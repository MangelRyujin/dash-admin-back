from django.conf import settings

def format_frontend_url(path):
    front_url = settings.FRONTEND_URL
    return f"{front_url}{path}"
