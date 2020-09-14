from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.validators import UniqueValidator

from accounts.models import User, FileModel
from accounts.utils import URLEnDecrypt


class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class FileManageSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)
    name = serializers.CharField()

    class Meta:
        model = FileModel
        fields = ['file', 'name']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        encrypted_path = URLEnDecrypt.encrypt(instance.file.name)
        ret['url'] = reverse('polls:download', args=[encrypted_path], request=self.context['request'])
        return ret
