from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator

from accounts.models import FileModel
from accounts.utils import URLEnDecrypt


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['username', 'email']


class FileManageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    patient_name = serializers.CharField(required=True)
    file = serializers.FileField(use_url=False)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FileModel
        fields = ['user', 'patient_name', 'file', 'created_at']
        read_only_fields = ['user']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        encrypted_path = URLEnDecrypt.encrypt(str(instance.id))
        ret['url'] = reverse('polls:download', args=[encrypted_path], request=self.context['request'])
        return ret

    def create(self, validated_data: dict):
        try:
            file_obj = FileModel.objects.create(**validated_data)
        except Exception:
            raise
        return file_obj
