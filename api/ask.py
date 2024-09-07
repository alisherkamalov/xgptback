from django.core.wsgi import get_wsgi_application

def handler(environ, start_response):
    application = get_wsgi_application()
    return application(environ, start_response)
