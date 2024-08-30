import json
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog

class RequestLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Only log requests to endpoints starting with '/api'
        if request.path.startswith('/api'):
            request.log = {
                'endpoint': request.path,
                'method': request.method,
                'headers': json.dumps(dict(request.headers)),
                'payload': json.dumps(request.body.decode('utf-8') if request.body else {}),
            }

    def process_response(self, request, response):
        # Only process response logging if a request log was created
        if hasattr(request, 'log'):
            log = request.log
            log['response'] = json.dumps(response.content.decode('utf-8'))
            log['status_code'] = response.status_code
            RequestLog.objects.create(**log)
        return response
