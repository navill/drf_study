from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=False)


class FileModel(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField()
