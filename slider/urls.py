from django.urls import path
from slider.views import (
    slider_view,
    manage_sliders_view,

    upload_image,
    admin_slider,
    user_slider,
)

app_name = 'slider'

urlpatterns = [
    # path('', slider_view, name='slider'),
    # path('manage_sliders/', manage_sliders_view, name='manage_sliders'),
    # path('slider/', slider_view, name='slider'),

    path('upload/', upload_image, name='upload_image'),
    path('admin/slider/', admin_slider, name='admin_slider'),
    path('slider/', user_slider, name='user_slider'),
]