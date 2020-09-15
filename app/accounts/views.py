# Create your views here.
import mimetypes
import os
import urllib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import FileResponse
from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import FileModel
from accounts.permissions import OwnerOnlyAccess
from accounts.serializers import UserCreateSerializer, FileManageSerializer
from accounts.utils import URLEnDecrypt


@api_view(['GET', 'POST'])
def create_user_view(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'ok'})
    else:
        return Response({'messgae': 'error'})


class TestGenericView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FileView(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileManageSerializer
    permission_classes = [OwnerOnlyAccess]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        file_serializer = FileManageSerializer(data=request.data, context={'request': request})
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            queryset = queryset.filter(user=self.request.user)
        return queryset


@login_required
def download(request, path):
    # todo: request.user에 따른 authentication
    # login_required + owner = can access
    # if OwnerOnlyAccess.has_object_permission(request, _, _):
    #     pass
    decrypted_url = URLEnDecrypt.decrypt(path)
    decrypted_path = urllib.parse.unquote(decrypted_url)

    file_name = get_filename(decrypted_path)
    file_path = get_full_path(decrypted_path)

    if os.path.exists(file_path):
        file_handler = open(file_path, 'rb')
        response = create_file_response(file_handler, file_name, file_path)
        return response
    else:
        raise FileNotFoundError('Invalid file path')


def get_full_path(path):
    return os.path.join(settings.MEDIA_ROOT, path)


def get_filename(path):
    if ' ' in path:
        path = path.replace(' ', '_')
    splited_url = path.split('/')
    file_name = splited_url[-1]
    return file_name


def create_file_response(handler, file_name, path):
    mime_type, _ = mimetypes.guess_type(file_name)
    file_name = urllib.parse.quote(file_name.encode('utf-8'))

    response = FileResponse(handler, content_type=mime_type)
    response['Content-Length'] = str(os.path.getsize(path))
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_name)
    return response
