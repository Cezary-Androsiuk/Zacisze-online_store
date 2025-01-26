from django.db import models

# class SliderItem(models.Model):
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     order = models.PositiveIntegerField(default=0)
#     in_use = models.BooleanField(null=False, blank=True, default=False)
#     # product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     pass

# class Slider(models.Model):
#     products = models.ManyToManyField(Product, through='SliderItem')
    
# class Sliders(models.Model):
#     sliders = models.


# class Image(models.Model):
#     title = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='slider_images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
    
# class Slider(models.Model):
#     name = models.CharField(max_length=255)
#     images = models.ManyToManyField(Image, through='SliderImage')
#     created_at = models.DateTimeField(auto_now_add=True)

# class SliderImage(models.Model):
#     slider = models.ForeignKey(Slider, on_delete=models.CASCADE)
#     image = models.ForeignKey(Image, on_delete=models.CASCADE)
#     order = models.PositiveIntegerField(default=0)

class SliderImage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='slider_images/')
    isInSlider = models.BooleanField()
