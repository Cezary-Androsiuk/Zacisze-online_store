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
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('must_authenticate')
    
    # get all sliders
    # products = Product.objects.all()
    # products = Product.objects.filter(is_deleted=False)
    
    # for each slider read all products
    # for product in products:
    #     product.title = product.title[:40] + '...' if len(product.title) > 40 else product.title
    #     product.authors = product.authors[:50] + '...' if len(product.authors) > 50 else product.authors

    context = {'sliders': ['slider1', 'slider2']}
    return render(request, "manage_sliders.html", context)




# from django.shortcuts import render, redirect
from .models import SliderImage
from .forms import SliderImageForm

# import pprint

def upload_image(request):
    if request.method == 'POST':
        form = SliderImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')
    else:
        form = SliderImageForm()
    return render(request, 'upload_image.html', {'form': form})

def admin_slider(request):
    print("slider loaded, request:")
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(vars(request))
    sliderImages = SliderImage.objects.all();
    print(sliderImages)
    return render(request, 'admin_slider.html', {'images': sliderImages})

def user_slider(request):
    sliderImages = SliderImage.objects.filter(isInSlider = True);
    print(sliderImages)
    return render(request, 'user_slider.html', {'images': sliderImages})