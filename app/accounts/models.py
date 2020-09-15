import datetime

from django.contrib.auth.models import User
from django.db import models


# todo: 날짜-> staff -> patient -> 파일이름_시간.ext 구조로 저장
def user_directory_path(instance, filename):
    day, time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S').split('_')
    name, ext = filename.split('.')
    return f'{day}/{instance.user}/{instance.patient_name}/{name}_{time}.{ext}'


class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
