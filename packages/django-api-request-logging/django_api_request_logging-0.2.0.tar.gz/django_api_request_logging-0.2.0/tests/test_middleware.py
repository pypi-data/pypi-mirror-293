from django.test import TestCase, Client
from request_logging_module.models import RequestLog

class RequestLoggingMiddlewareTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_request_logging(self):
        response = self.client.get('/some-endpoint/')
        self.assertEqual(response.status_code, 200)
        log = RequestLog.objects.first()
        self.assertIsNotNone(log)
        self.assertEqual(log.endpoint, '/some-endpoint/')