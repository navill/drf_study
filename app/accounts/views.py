# Create your views here.
import os

from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import User, FileModel
from accounts.serializers import UserCreateSerializer, FileManageSerializer


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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)


class FileView(ListModelMixin, RetrieveModelMixin, GenericAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileManageSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = ['pk']

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        instance = self.queryset.get(id=pk)
        file_handle = instance.file.open()

        # send file
        response = FileResponse(file_handle, content_type='multipart/formed-data')
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name
        return response

    def post(self, request, *args, **kwargs):
        file_serializer = FileManageSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = Response(f.read(), content_type='multipart/formed-data')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        raise Exception
