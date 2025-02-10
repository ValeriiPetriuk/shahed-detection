from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class VideoStreamView(LoginRequiredMixin, TemplateView):
    template_name = 'detection/connect.html'
  

# def stream():
#     cap = cv2.VideoCapture('video/1.mp4')
#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             print("Error reading")
#             break
        
#         image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  

import time
def stream():
    while True:
        cap = cv2.VideoCapture(1)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_time = 1 / fps  

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  
            
            time.sleep(frame_time)  

        cap.release()
            

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')    



# class VideoCamera:
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#         self.lock = threading.Lock()  # Блокування для синхронізації доступу
#         self.running = True

#         # Запускаємо окремий потік для читання кадрів
#         self.thread = threading.Thread(target=self.update, daemon=True)
#         self.thread.start()

#     def update(self):
#         """Оновлює кадри в окремому потоці."""
#         while self.running:
#             with self.lock:
#                 self.ret, self.frame = self.video.read()

#     def get_frame(self):
#         """Повертає поточний кадр."""
#         with self.lock:
#             if self.ret:
#                 _, jpeg = cv2.imencode('.jpg', self.frame)
#                 return jpeg.tobytes()
#             else:
#                 return None

#     def stop(self):
#         """Зупиняє відеопотік."""
#         self.running = False
#         self.video.release()


# class VideoStreamView(LoginRequiredMixin, TemplateView):
#     template_name = 'detection/connect.html'
    
#     # @csrf_exempt
#     # def post(self, request, *args, **kwargs):
#     #     uploaded_file = request.FILES.get('file')  
#     #     print("uploaded file:", uploaded_file)
#     #     return render(request, 'detection/connect.html')

# def stream():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()

#         if not ret:
#             print("Error reading")
#             break
        
#         image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  

# def video_feed(request):
#     return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')    



# class VideoCamera:
#     def __init__(self, rtsp_url):
#         self.video = cv2.VideoCapture(rtsp_url)

#     def get_frame(self):
#         success, frame = self.video.read()
#         if not success:
#             return None

#         _, jpeg = cv2.imencode(".jpg", frame)
#         return jpeg.tobytes()

# def generate_frames(camera):
#     while True:
#         frame = camera.get_frame()
#         if frame is None:
#             break
#         yield (b"--frame\r\n"
#                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

# @csrf_exempt
# def video_feed(request):
#     rtsp_url = request.session.get("rtsp_url", None)
#     print('rtsp_url:', rtsp_url)
#     if not rtsp_url:
#         return StreamingHttpResponse(status=404)

#     return StreamingHttpResponse(generate_frames(VideoCamera(rtsp_url)),
#                                  content_type="multipart/x-mixed-replace; boundary=frame")

# def connect_to_camera(request):
#     if request.method == "POST":
#         form = RTSPForm(request.POST)
#         if form.is_valid():
#             request.session["rtsp_url"] = form.cleaned_data["rtsp_url"]
#             return redirect("home")

#     else:
#         form = RTSPForm()

#     return render(request, "detection/connect.html", {"form": form})


# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.generic import TemplateView

# # Create your views here.
# import cv2
# from django.http import StreamingHttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views import View
# from detection.forms import RTSPForm
# from django.shortcuts import redirect

# from django.core.cache import cache

# class VideoCamera:
#     def __init__(self, RTSP_URL):
#         self.video = cv2.VideoCapture(RTSP_URL)
    
#     def __del__(self):
#         if self.video:
#             self.video.release()
    
#     def get_frame(self):
#         if not self.video:
#             return None
#         success, frame = self.video.read()
#         if not success:
#             return None
#         _, jpeg = cv2.imencode(".jpg", frame)
#         return jpeg.tobytes()

# def connect_to_camera(request):
#     if request.method == "POST":
#         form = RTSPForm(request.POST)
#         if form.is_valid():
#             cache.set(f"rtsp_url_{request.user.id}", form.cleaned_data["rtsp_url"], timeout=3600)
#             return redirect("video_feed")

#     else:
#         initial_url = cache.get(f"rtsp_url_{request.user.id}")
#         form = RTSPForm(initial={"rtsp_url": initial_url})

#     return render(request, "detection/connect.html", {"form": form})

# def generate_frames(camera):
#     while True:
#         frame = camera.get_frame()
#         if frame:
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# class VideoStreamView(View):
#     @csrf_exempt
#     def get(self, request, *args, **kwargs):
#         rtsp_url = cache.get(f"rtsp_url_{request.user.id}")
#         return StreamingHttpResponse(generate_frames(VideoCamera(rtsp_url)), content_type="multipart/x-mixed-replace; boundary=frame")


# # RTSP_URL = "rtsp://username:password@ip_address:port/stream"

# # class VideoCamera:
# #     def __init__(self):
# #         self.video = cv2.VideoCapture(0)
    
# #     def __del__(self):
# #         self.video.release()
    
# #     def get_frame(self):
# #         success, frame = self.video.read()
# #         if not success:
# #             return None
# #         _, jpeg = cv2.imencode('.jpg', frame)
# #         return jpeg.tobytes()

# # def generate_frames(camera):
# #     while True:
# #         frame = camera.get_frame()
# #         if frame:
# #             yield (b'--frame\r\n'
# #                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# # class VideoStreamView(View):
# #     @csrf_exempt
# #     def get(self, request, *args, **kwargs):
# #         return StreamingHttpResponse(generate_frames(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')


# # # def home(request):
# # #     return render(request, 'detection/main.html')

# # class ConnectToCameraView(TemplateView):
# #     template_name = 'detection/connect.html'