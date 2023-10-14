from django.db import models

class Document(models.Model):
    file_name = models.CharField(max_length=200, default='')
    file_extension = models.CharField(max_length=10, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)

