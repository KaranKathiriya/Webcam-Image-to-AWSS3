from django.urls import path
from . import views
from django.http import StreamingHttpResponse


urlpatterns = [
    path('', views.home, name='index'),
    path('capture_img', views.capture_img, name='capture_img'),
]
