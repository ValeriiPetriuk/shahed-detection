from django.http import StreamingHttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from detection.camera import  stream_video
from detection.models import Detection, Camera
from django.db.models import Count
from django.db.models.functions import TruncDate


class VideoStreamView(LoginRequiredMixin, TemplateView):
    template_name = 'detection/connect.html'
  


def video_feed(request, pk):
    try:
        camera = Camera.objects.get(pk=pk)
        return StreamingHttpResponse(stream_video(camera), content_type='multipart/x-mixed-replace; boundary=frame') 
    except:
        pass
   


class CameraList(LoginRequiredMixin, ListView):
    model = Camera
    template_name = 'detection/camera_list.html'
    

class StatisticsView(LoginRequiredMixin, ListView):
    model = Detection
    template_name = 'detection/statistics.html'
    paginate_by = 5
    ordering = ['-time']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chart_data = (
            Detection.objects
            .annotate(date=TruncDate('time'))
            .values('date')
            .annotate(total=Count('id'))
            .order_by('date')
        )
        context['chart_labels'] = [entry['date'].strftime('%d-%m-%Y') for entry in chart_data]
        context['chart_values'] = [entry['total'] for entry in chart_data]
        
        return context


class DetailDetection(LoginRequiredMixin, DetailView):
    model = Detection
    template_name = 'detection/detail.html'
    context_object_name = 'detection'