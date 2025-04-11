from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} location {self.location}"




class Detection(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/detection')
    precision = models.FloatField(default=0.0)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, blank=True, null=True, related_name='cameras')
    

    # def __str__(self):
    #     return f'Detection at {self.time} - {self.count} shades detected in {self.camera.location}'