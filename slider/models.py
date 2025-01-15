from django.db import models

from store.models import (
    Product
)

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
