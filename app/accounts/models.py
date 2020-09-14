from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from accounts.utils import URLEnDecrypt


class User(models.Model):
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=False)


class FileModel(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField()
    file_url = models.CharField(max_length=255, default='')


@receiver(pre_save, sender=FileModel)
def pre_save_user(sender, instance, **kwargs):
    url = URLEnDecrypt.encrypt(instance.file.url)  # /storage/alskdjrakldf....
    a = reverse('polls:download', args=(url,))
    print(a)
    instance.file_url = url

