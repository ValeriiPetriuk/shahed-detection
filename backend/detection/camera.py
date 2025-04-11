import threading
import cv2
from ultralytics import YOLO
from datetime import datetime
import time
import os 
from detection.models import Detection
from django.core.files.base import ContentFile
from detection.bot.bot import send_msg



def stream(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

def save_detection(frame, camera, precision, count):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_folder = "media/images/detection"

    
    os.makedirs(image_folder, exist_ok=True)

    image_filename = f"detection_{timestamp}.jpg"
    image_path = os.path.join(image_folder, image_filename)

    cv2.imwrite(image_path, frame)

    detection = Detection(
        camera=camera,
        precision=precision,
        count=count
    )

    with open(image_path, "rb") as img_file:
        detection.image.save(image_filename, ContentFile(img_file.read()), save=True)
    return detection, image_path


# def stream_video(camera, source=None):
#     model = YOLO("detection/modelAI/best.pt", verbose=False)
#     cap = cv2.VideoCapture(camera.source)
#     shahed_detection_prev = False
#     detection_start_time = None  # Час початку детекції
#     detection_threshold = 3  # Час (секунди) для підтвердження детекції
    
#     while True:
#         count_current_obj = 0
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         frame_time = 1 / fps if fps > 0 else 0.1
        
#         ret, frame = cap.read()
#         if not ret:
#             print('video restarting...')
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue
        
#         results = model.track(frame, conf=0.3)
#         annotated_frame = results[0].plot()
        
#         conf_scores = results[0].boxes.conf.tolist() if results[0].boxes.conf is not None else []
#         mean_conf = sum(conf_scores) / len(conf_scores) if conf_scores else 0.0
#         shahed_detected = any(result for result in results for obj in result.boxes if obj.cls in (0,))
        
#         if shahed_detected:
#             if detection_start_time is None:
#                 detection_start_time = time.time()  # Запускаємо таймер
#             elif time.time() - detection_start_time >= detection_threshold:
#                 if not shahed_detection_prev:
#                     detection_save, image_path = save_detection(annotated_frame, camera=camera, precision=round(mean_conf, 2), count=len(conf_scores))
#                     send_msg.delay(image_path, detection_save.pk)
#                 shahed_detection_prev = True
#         else:
#             detection_start_time = None  # Скидаємо таймер
#             shahed_detection_prev = False
        
#         image_bytes = cv2.imencode('.jpg', annotated_frame)[1].tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
        
#         time.sleep(frame_time)


def stream_video(camera, source=None):
    model = YOLO("detection/modelAI/best.pt", verbose=False) 
    
    cap = cv2.VideoCapture(camera.source)
    shahed_detection_prev = False


    while True:  
        count_current_obj = 0
        # cap = cv2.VideoCapture(1)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_time = 1 / fps  

        
        ret, frame = cap.read()
        if not ret:
            print('video restarting...')
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        results = model.track(frame, conf=0.3)
        annotated_frame  = results[0].plot()

        conf_scores = results[0].boxes.conf.tolist() if results[0].boxes.conf is not None else []
        mean_conf = sum(conf_scores) / len(conf_scores) if conf_scores else 0.0
        shahed_detected = any(result for result in results for obj in result.boxes if obj.cls in (0,))
        
        if shahed_detected and not shahed_detection_prev:
            detection_save, image_path = save_detection(annotated_frame, camera=camera, precision=round(mean_conf, 2), count=len(conf_scores))   
            send_msg.delay(image_path, detection_save.pk)
        
        shahed_detection_prev = shahed_detected

        image_bytes = cv2.imencode('.jpg', annotated_frame)[1].tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  

        time.sleep(frame_time)  

  


# def stream_video(camera, source=None):
#     model = YOLO("detection/modelAI/best.pt", verbose=False)
#     cap = cv2.VideoCapture(camera.source)
#     shahed_detection_prev = False
#     prev_count_obj = 1  # Змінна для відстеження попередньої кількості об'єктів

#     while True:
#         count_current_obj = 0
#         fps = cap.get(cv2.CAP_PROP_FPS)
#         frame_time = 1 / fps if fps > 0 else 0.03  # Уникаємо ділення на 0

#         ret, frame = cap.read()
#         if not ret:
#             print('video restarting...')
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
#             continue

#         results = model.track(frame, conf=0.3)
#         annotated_frame = results[0].plot()

#         conf_scores = results[0].boxes.conf.tolist() if results[0].boxes.conf is not None else []
#         mean_conf = sum(conf_scores) / len(conf_scores) if conf_scores else 0.0

#         count_current_obj = len(conf_scores)

#         shahed_detected = any(obj.cls in (0,) for result in results for obj in result.boxes)
        
#         if shahed_detected and not shahed_detection_prev:
#             detection_save, image_path = save_detection(annotated_frame, camera=camera, precision=round(mean_conf, 2), count=count_current_obj)
#             send_msg.delay(image_path, detection_save.pk)
        
#         if count_current_obj > prev_count_obj:  # Якщо кількість об'єктів збільшилася
#             detection_save, image_path = save_detection(annotated_frame, camera=camera, precision=round(mean_conf, 2), count=count_current_obj)
#             send_msg.delay(image_path, detection_save.pk)

#         shahed_detection_prev = shahed_detected
#         prev_count_obj = count_current_obj  # Оновлюємо попередню кількість об'єктів

#         image_bytes = cv2.imencode('.jpg', annotated_frame)[1].tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')

#         time.sleep(frame_time)
