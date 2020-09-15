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
    file = serializers.FileField(use_url=False)
    # name = serializers.CharField()

    class Meta:
        model = FileModel
        fields = ['user', 'file']
        # read_only_fields = ['user_id']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        encrypted_path = URLEnDecrypt.encrypt(instance.file.name)
        ret['url'] = reverse('polls:download', args=[encrypted_path], request=self.context['request'])
        return ret

    def create(self, validated_data: dict):
        try:
            # user = self.context['request'].user
            file_obj = FileModel.objects.create(**validated_data)
        except Exception:
            raise
        return file_obj
