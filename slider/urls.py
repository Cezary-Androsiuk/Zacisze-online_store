from django.urls import path
from slider.views import (
    # slider_view,
    manage_sliders_view
)

app_name = 'slider'

urlpatterns = [
    # path('', slider_view, name='slider'),
    path('manage_sliders/', manage_sliders_view, name='manage_sliders'),
]