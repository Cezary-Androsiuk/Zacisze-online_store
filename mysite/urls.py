"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from personal.views import (
    home_screen_view,
    faqs_view,
    about_view,
)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
)

from store.views import (
    cart_view,
    checkout_view,
    reservation_view,
    order_summary_view,
    reservation_summary_view,
    reservations_list_view,
    orders_list_view,
    set_reservation_as_received_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', home_screen_view, name='home'),
    path('store/', include('store.urls', 'store')),
    
    path('login/', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account'),
    path('orders_list/', orders_list_view, name='orders_list'),
    path('reservations_list/', reservations_list_view, name='reservations_list'),
    path('set_reservation_as_received/<str:reservation_id>/', set_reservation_as_received_view, name='set_reservation_as_received'),
    path('must_authenticate/', must_authenticate_view, name='must_authenticate'),

    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    path('reservation/', reservation_view, name='reservation'),
    path('order_summary/', order_summary_view, name='order_summary'),
    path('reservation_summary/', reservation_summary_view, name='reservation_summary'),

    path('faqs/', faqs_view, name='faqs'),
    path('about/', about_view, name='about'),
    
    
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)