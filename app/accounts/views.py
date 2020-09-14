# Create your views here.
import mimetypes
import os
import urllib

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from accounts.models import User, FileModel
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
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    # url =
    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # get detail object
        response = super().retrieve(request, *args, **kwargs)
        url = response.data['file_url']
        response['url'] = reverse('polls:download', args=[url], request=request)
        # if: self._file_download -> donwload url 생성
        # else: 단순 retrieve
        # _file_download(response)
        return response

    def post(self, request, *args, **kwargs):
        file_serializer = FileManageSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def download(request, path2):
    decrypted_path = URLEnDecrypt.decrypt(path2)
    url = urllib.parse.unquote(decrypted_path)
    file_name, path = divide_url(url)

    if os.path.exists(path):
        file_handler = open(path, 'rb')
        response = create_file_response(file_handler, file_name, path)

        return response
    else:
        raise Exception


def divide_url(original_url):
    url = original_url
    if ' ' in original_url:
        url = original_url.replace(' ', '_')
    splited_url = url.split('/')
    file_name = splited_url[-1]
    path = os.path.join(settings.MEDIA_ROOT, file_name)
    return file_name, path


def create_file_response(handler, file_name, path):
    mime_type = mimetypes.guess_type(file_name)
    file_name = urllib.parse.quote(file_name.encode('utf-8'))
    response = FileResponse(handler, content_type=mime_type[0])
    response['Content-Length'] = str(os.path.getsize(path))
    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_name)
    return response
#
#
# def _file_download(response: dict):
#     instance = response.data.serializer.instance
#     file_handle = instance.file.open()
#     response = FileResponse(file_handle, content_type='multipart/octet-stream')
#     response['Content-Length'] = instance.file.size
#     response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name
