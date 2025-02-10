from django.urls import path
# from .views import VideoStreamView, ConnectToCameraView
from .views import VideoStreamView, video_feed
urlpatterns = [
    path('', VideoStreamView.as_view(), name='home'),
    path('video_feed/', video_feed, name='video_feed'),
]

# urlpatterns = [
#     path('', ConnectToCameraView.as_view()),
#     path('video_feed/', VideoStreamView.as_view(), name='video_feed'),
# ]