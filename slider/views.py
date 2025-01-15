from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings


from store.models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Reservation,
    ReservationItem,
)
from store.forms import (
    CreateProductForm,
    UpdateProductForm,
    OrderForm,
    ReservationForm,
)
from account.models import (
    Account,
)


def slider_view(request):
    return render(request, "store/store.html", {})


def manage_sliders_view(request):
    context = {}
    # user = request.user
    # if not user.is_authenticated or not user.is_staff:
    #     return redirect('must_authenticate')
    
    # get all sliders
    # products = Product.objects.all()
    # products = Product.objects.filter(is_deleted=False)
    
    # for each slider read all products
    # for product in products:
    #     product.title = product.title[:40] + '...' if len(product.title) > 40 else product.title
    #     product.authors = product.authors[:50] + '...' if len(product.authors) > 50 else product.authors

    # context = {'sliders': ['slider1', 'slider2']}
    return render(request, "slider/manage_sliders.html", context)

