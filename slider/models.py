from django.db import models

class SliderImage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='slider_images/')
    isInSlider = models.BooleanField()
