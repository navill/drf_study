import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.utils import URLEnDecrypt


def user_directory_path(instance, filename):
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    name, ext = filename.split('.')
    print('??')
    return '{0}/{1}_{2}.{3}'.format(instance.name, name, time, ext)


class User(models.Model):
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    email = models.EmailField(unique=True, null=False, blank=False)


class FileModel(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    file_url = models.CharField(max_length=255, default='')
