from django.db import models

class RequestLog(models.Model):
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    headers = models.TextField()
    payload = models.TextField()
    response = models.TextField()
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status_code}"