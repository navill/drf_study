import mimetypes
import os
import urllib

from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import FileResponse, HttpResponse
from oauth2_provider.views.mixins import ProtectedResourceMixin
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import FileModel
from accounts.permissions import OwnerOnlyAccess
from accounts.serializers import UserCreateSerializer, FileManageSerializer, UserSerializer
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
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FileView(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = FileModel.objects.all().order_by('-created_at')
    serializer_class = FileManageSerializer
    permission_classes = [IsAuthenticated, OwnerOnlyAccess]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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


def download(request, path):
    file_id = get_file_id(path)
    file_obj = FileModel.objects.get(id=file_id)
    if file_obj.user == request.user:
        try:
            # file_handler = open(file_path, 'rb')
            handler = file_obj.file.open()
            response = create_file_response(handler)
            return response
        except Exception:
            raise FileNotFoundError('Invalid file path')
    # return Response()  # for drf
    return HttpResponse('can not access this url', status=status.HTTP_401_UNAUTHORIZED)


def get_file_id(path):
    decrypted_url = URLEnDecrypt.decrypt(path)
    return urllib.parse.unquote(decrypted_url)


def create_file_response(handler):
    file_name = os.path.basename(handler.name)
    mime_type, _ = mimetypes.guess_type(file_name)
    quoted_name = urllib.parse.quote(file_name.encode('utf-8'))

    response = FileResponse(handler, content_type=mime_type)
    response['Content-Length'] = handler.size
    response['Content-Disposition'] = 'attachment; filename=' + quoted_name
    return response

