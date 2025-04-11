from django.urls import path
# from .views import VideoStreamView, ConnectToCameraView
from .views import VideoStreamView, video_feed, StatisticsView, DetailDetection, CameraList
urlpatterns = [ 
    path('', CameraList.as_view(), name='camera_list'),
    # path('', VideoStreamView.as_view(), name='home'),
    
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('video_feed/<int:pk>/', video_feed, name='video_feed'),
    path('statistics/detection/<int:pk>/', DetailDetection.as_view(), name='detection-detail'),
]

