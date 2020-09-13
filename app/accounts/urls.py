from django.urls import path

from accounts.views import create_user_view, TestGenericView, FileView

app_name = 'polls'

urlpatterns = [
    path('user/create/', create_user_view),
    path('test/', TestGenericView.as_view(), name='test'),
    path('upload/<int:pk>', FileView.as_view(), name='download'),
    path('upload/', FileView.as_view(), name='upload'),
]
