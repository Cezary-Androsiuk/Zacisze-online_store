from django.shortcuts import render, redirect

from account.models import (
    Account
)

from store.models import (
    Product,
    OrderItem,
    ReservationItem,
)

# Create your views here.
def home_screen_view(request):
    context = {}

    NUMBER_OF_HIGHLITED_ITEMS = 3

    products_count = {}

    orders_items = OrderItem.objects.all()
    for item in orders_items:
        product = item.product
        if product.title in products_count:
            products_count[product.title] += item.quantity
        else:
            products_count[product.title] = item.quantity

    reservations_items = ReservationItem.objects.all()
    for item in reservations_items:
        product = item.product
        if product.title in products_count:
            products_count[product.title] += item.quantity
        else:
            products_count[product.title] = item.quantity

    # print(products_count)
    products_count = sorted(products_count.items(), key=lambda x: x[1], reverse=True)

    products = []
    for product_name, count in products_count[:NUMBER_OF_HIGHLITED_ITEMS]:
        products.append(Product.objects.get(title=product_name))
    
    context['products'] = products

    return render(request, "personal/home.html", context)


def faqs_view(request):
    context = {}

    return render(request, "personal/faqs.html", context)


def about_view(request):
    context = {}

    return render(request, "personal/about.html", context)


def color_view(request):
    context = {}
    user = request.user
    if not user.is_authenticated or not user.is_admin:
        return redirect('must_authenticate')

    return render(request, "personal/colors.html", context)