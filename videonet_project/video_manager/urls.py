from django.urls import path
from .views import video_detail, video_list, create_video, update_video, delete_video

urlpatterns = [
    path('', video_list, name='video_list'),
    path('video/nuevo/', create_video, name='create_video'),
    path('video/<int:pk>/editar/', update_video, name='update_video'),
    path('video/<int:pk>/eliminar/', delete_video, name='delete_video'),
    path('video/<int:pk>/', video_detail, name='video_detail'),
]
