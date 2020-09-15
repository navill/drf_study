import datetime

from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    name, ext = filename.split('.')
    return '{0}/{1}_{2}.{3}'.format(instance.user, name, time, ext)


# class User(models.Model):
#     first_name = models.CharField(max_length=12)
#     last_name = models.CharField(max_length=12)
#     email = models.EmailField(unique=True, null=False, blank=False)


class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    # file_url = models.CharField(max_length=255, default='')
