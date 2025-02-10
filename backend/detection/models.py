from django.db import models


class Detection(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/detection')
    precision = models.FloatField(default=0.0)
    