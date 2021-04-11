from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    file_name = models.TextField(blank=True, null=True)