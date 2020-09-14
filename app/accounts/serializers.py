from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import User, FileModel


class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class FileManageSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    name = serializers.CharField()
    file_url = serializers.CharField()

    class Meta:
        model = FileModel
        fields = ['file', 'name', 'file_url']
