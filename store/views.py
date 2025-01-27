from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.conf import settings


from store.models import *
from store.forms import (
    CreateProductForm,
    UpdateProductForm,
    OrderForm,
    ReservationForm,
)
from account.models import (
    Account,
)




def store_view(request):
    # delete product feature
    products = Product.objects.all()
    # products = Product.objects.filter(is_deleted=False)
    for product in products:
        product.title = product.title[:40] + '...' if len(product.title) > 40 else product.title
        product.authors = product.authors[:50] + '...' if len(product.authors) > 50 else product.authors
        
        if request.user.is_staff:
            relatedComments = Comment.objects.filter(product=product, confirmed=False)
            product.containsNotConfirmedComments = relatedComments.count()
        else:
            product.containsNotConfirmedComments = 0

    context = {'products': products}
    return render(request, "store/store.html", context)




def create_product_view(request):
    print(request)
    context = {}
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('must_authenticate')
    
    # what will be send while submitting a form
    form = CreateProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        productExist = Product.objects.filter(title=form.getTitle()).exists() # check if product with that name exist
        if productExist:
            # print("product exist :<")
            # context['error_info'] = "product already exist"
            pass
        else:
            obj = form.save(commit=False) # commit to have time to add author after we check if form is valid
            obj.added_by = Account.objects.filter(email=user.email).first()
            obj.save() # save created object to db
            return redirect('store:store')
    else:
        # print("form invalid :<")
        # context['error_info'] = "form invalid"
        pass

    
    context['form'] = form
    return render(request, 'store/create_product.html', context)


def view_product_view(request, slug):
    context = {}
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    all_comments = Comment.objects.filter(product=product)
    out_comments = []

    for comment in all_comments:
        if user.is_staff: # staff stuff
            out_comments.append(comment)

        else: # auth user and guest stuff
            # user could be None
            current_user = user if user.is_authenticated else None
            if comment.user == current_user or comment.confirmed == True:
                out_comments.append(comment)

    context['product'] = product
    context['comments'] = out_comments
    
    success_update_message = request.session.get('success_update_message')
    if success_update_message:
        if request.user.is_staff:
            context['success_update_message'] = success_update_message
        del request.session['success_update_message']

    return render(request, 'store/view_product.html', context)


def edit_product_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('must_authenticate')
    
    product = get_object_or_404(Product, slug=slug)

    if request.POST:
        # what will be send while submiting a form
        form = CreateProductForm(request.POST or None, request.FILES or None, instance=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save() # save created object to db
            product = obj
            request.session['success_update_message'] = 'Updated'
            return redirect('store:view_product', slug=slug)
            # return redirect('store:view_product')

    form = UpdateProductForm(
        initial={
            'title': product.title,
            'authors': product.authors,
            'description': product.description,
            'price': product.price,
            'image': product.image,
        }
    )
        
    context['form'] = form

    return render(request, 'store/edit_product.html', context)


def add_comment_view(request, slug):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('must_authenticate')
    
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        content = request.POST.get('content')
        if not content == '':
            comment = Comment.objects.create(
                user = user,
                product = product,
                content = content
            )
            comment.save()

    return redirect('store:view_product', slug=comment.product.slug)

def confirm_comment_view(request, comment_id):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('must_authenticate')
    
    comment = get_object_or_404(Comment, id=comment_id)
    comment.confirmed = True
    comment.save()
    return redirect('store:view_product', slug=comment.product.slug)

def add_reply_view(request, comment_id):
    user = request.user
    if not user.is_authenticated or not user.is_staff:
        return redirect('must_authenticate')
    
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        content = request.POST.get('content')
        if not content == '':
            reply = Reply.objects.create(
                user = user,
                parentComment = comment,
                content = content
            )
            reply.save()

    return redirect('store:view_product', slug=comment.product.slug)


def delete_product_view(request, slug):
    context = {}
    if not request.user.is_staff:
        return redirect('must_authenticate')
    product = Product.objects.filter(slug=slug).first()

    product.title = product.title[:40] + '...' if len(product.title) > 40 else product.title
    product.authors = product.authors[:50] + '...' if len(product.authors) > 50 else product.authors

    context['product'] = product

    return render(request, 'store/delete_product_confirm.html', context)



def delete_product_confirmed_view(request, slug):
    if not request.user.is_staff:
        return redirect('must_authenticate')
    
    # if not request.POST:
    #     return render(request, 'store/delete_product_confirm.html', context)
    
    # action = str(request.POST.get('confirm_button'))
    action = 'delete'
    if action == 'delete':
        try:
            # delete product feature
            Product.objects.get(slug=slug).delete() # we do not delete products here 
            # product = Product.objects.get(slug=slug)
            # product.is_deleted = True
            # product.save()
        except Exception as e:
            print(f"Error while deleting Product(slug={slug}) from database: {e}")
        return redirect('store:store')
    
    elif action == 'cancel':
        return redirect('store:store')
        





def add_to_cart_view(request, slug):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('must_authenticate')
    # get cart associeted with current user
    #   that is not staff and is authenticated
    user_cart = Cart.objects.get(user=request.user)
    # get product that i want to add to cart
    product_to_update = Product.objects.get(slug=slug)

    # delete product feature
    # if product_to_update.is_deleted:
    #     print('error! product is deleted')
    #     return redirect('cart')    

    #* create (if not exist) group of objects that is added to cart, or increment/decrement quantity 
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product_to_update)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

def rm_from_cart_view(request, slug):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('must_authenticate')
    
    user_cart = Cart.objects.get(user=request.user)
    product_to_update = Product.objects.get(slug=slug)

    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product_to_update)
    # if was created ten quantity==1 decrementing makes it 0, 
    # if was 1 then will be deleted and if cart_item does not exist then also item will be deleted from cart -> all fine
    cart_item.quantity -= 1
    cart_item.save()
    if cart_item.quantity <= 0:
        cart_item.delete()

    return redirect('cart')

def rm_cart_item_view(request, slug):
    if not request.user.is_authenticated or request.user.is_staff:
        return redirect('must_authenticate')
    
    user_cart = Cart.objects.get(user=request.user)
    product_to_update = Product.objects.get(slug=slug)

    CartItem.objects.filter(cart=user_cart, product=product_to_update).delete()

    return redirect('cart')





def cart_view(request): 
    if request.user.is_authenticated:
        is_ns = not request.user.is_staff
        is_na = not request.user.is_admin
        is_nsu = not request.user.is_superuser
        if is_ns and is_na and is_nsu:
            context = {}

            cart = Cart.objects.get(user=request.user)
            context['cart'] = cart
            context['cart_items'] = CartItem.objects.filter(cart=cart)
            # context['cart_total'] = cart.get_cart_total()

            return render(request, 'store/cart.html', context)
        
    return redirect('must_authenticate')

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    context = {}

    cart = Cart.objects.get(user=request.user)
    if not cart.cartitem_set.exists():
        return redirect('cart')
    context['cart'] = cart
    context['cart_items'] = CartItem.objects.filter(cart=cart)

    if request.POST:
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_data = {
                'first_name': order_form.cleaned_data['first_name'],
                'last_name': order_form.cleaned_data['last_name'],
                'address': order_form.cleaned_data['address'],
                'country': order_form.cleaned_data['country'],
                'city': order_form.cleaned_data['city'],
                'zip_code': order_form.cleaned_data['zip_code'],
                'card_name': order_form.cleaned_data['card_name'],
                'card_id': order_form.cleaned_data['card_id'],
                'card_exp': order_form.cleaned_data['card_exp'],
                'card_cvv': order_form.cleaned_data['card_cvv'],
            }
            
            print('order_form is valid!')
            order = cart.create_order(order_data)
            print('saving an order...')
            order.save()
            print('...order saved!')

            cart.products.clear()

            return redirect('order_summary')
        else:
            print("\tinvalid form!")
            print(order_form.errors)
    else:
        order_form = OrderForm()


    if settings.DEBUG:
        context['default'] = {
            'first_name': 'Janek',
            'last_name': 'Kowalski',
            'address': 'Mokry Dwór 5 m 6',
            'country': 'Poland',
            'city': 'Wrocław',
            'zip': '52-051',
            'card_name': 'Janek Kowalski',
            'card_id': '7896 4563 4213 2457',
            'card_exp': '13/99',
            'card_cvv': '123',
        }

    return render(request, 'store/checkout.html', context)

def reservation_view(request):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    context = {}

    cart = Cart.objects.get(user=request.user)
    if not cart.cartitem_set.exists():
        return redirect('cart')
    context['cart'] = cart
    context['cart_items'] = CartItem.objects.filter(cart=cart)
    

    if request.POST:
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation_data = {
                'first_name': reservation_form.cleaned_data['first_name'],
                'last_name': reservation_form.cleaned_data['last_name'],
                'address': reservation_form.cleaned_data['address'],
                'country': reservation_form.cleaned_data['country'],
                'city': reservation_form.cleaned_data['city'],
                'zip_code': reservation_form.cleaned_data['zip_code'],
            }
            
            print('reservation_form is valid!')
            reservation = cart.create_reservation(reservation_data)
            print('saving an reservation...')
            reservation.save()
            print('...reservation saved!')

            cart.products.clear()

            return redirect('reservation_summary')
        else:
            print("\tinvalid form!")
            print(reservation_form.errors)
    else:
        reservation_form = ReservationForm()

    
    if settings.DEBUG:
        context['default'] = {
            'first_name': 'Janek',
            'last_name': 'Kowalski',
            'address': 'Mokry Dwór 5 m 6',
            'country': 'Poland',
            'city': 'Wrocław',
            'zip': '52-051',
        }

    return render(request, 'store/reservation.html', context)

def order_summary_view(request):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    context = {}
    order = Order.objects.filter(user=request.user).order_by('-order_date').first()
    if not order.orderitem_set.exists():
        return redirect('cart')
    
    if order.delivered:
        return redirect('cart')
    
    context['order'] = order
    context['order_items'] = OrderItem.objects.filter(order=order)
    return render(request, 'store/order_summary.html', context)


def reservation_summary_view(request):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    context = {}
    reservation = Reservation.objects.filter(user=request.user).order_by('-reservation_date').first()
    if not reservation.reservationitem_set.exists():
        return redirect('cart')
    if reservation.received:
        return redirect('cart')
    
    context['reservation'] = reservation
    context['reservation_items'] = ReservationItem.objects.filter(reservation=reservation)
    return render(request, 'store/reservation_summary.html', context)

    
    

def orders_list_view(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('must_authenticate')
    
    context = {}
    
    keywords = request.GET.get('keywords', '')
    search_category = request.GET.get('search_category', '')
    display_delivered = 'display_delivered' in request.GET

    # handle clear button
    if 'search_clear' in request.GET:
        keywords = ''
        search_category = ''
        display_delivered = False

    # for reuse (fill form again) in frontend 
    context['keywords'] = keywords
    context['search_category'] = search_category
    context['display_delivered'] = display_delivered 

    if search_category == '1': # by 'ID' # OK
        if display_delivered:
            tmp_orders = Order.objects.all()
        else:
            tmp_orders = Order.objects.filter(delivered=False)
        # look for ID's that contains keyword
        orders = []
        for order in tmp_orders:
            if keywords in str(order.id):
                orders.append(order)

    elif search_category == '2': # by 'Email' # OK
        if display_delivered:
            orders = Order.objects.filter(user__email__contains=keywords)
        else:
            orders = Order.objects.filter(user__email__contains=keywords, delivered=False)

    elif search_category == '3': # by 'Order Name'
        if display_delivered:
            tmp_orders = Order.objects.all()
        else:
            tmp_orders = Order.objects.filter(delivered=False)
        
        # look for ID's that contains keyword
        orders = []
        for order in tmp_orders:
            if keywords.lower() in (str(order.first_name) + ' ' + str(order.last_name)).lower():
                orders.append(order)

    else:
        if display_delivered:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(delivered=False)
        
    context['orders'] = orders
 
    return render(request, 'store/orders_list.html', context)


def reservations_list_view(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('must_authenticate')
    
    context = {}
    
    # search form
    if request.POST:
        reservation_id = request.POST.get('reservation_id', '')
        reservation_object = Reservation.objects.filter(id=reservation_id)
        reservation_object.received = True
        reservation_object.save()
        

    keywords = request.GET.get('keywords', '')
    search_category = request.GET.get('search_category', '')
    display_received = 'display_received' in request.GET

    # handle clear button
    if 'search_clear' in request.GET:
        keywords = ''
        search_category = ''
        display_received = False

    # for reuse (fill form again) in frontend 
    context['keywords'] = keywords
    context['search_category'] = search_category
    context['display_received'] = display_received 

    if search_category == '1': # by 'ID' # OK
        if display_received:
            tmp_reservations = Reservation.objects.all()
        else:
            tmp_reservations = Reservation.objects.filter(received=False)
        # look for ID's that contains keyword
        reservations = []
        for reservation in tmp_reservations:
            if keywords in str(reservation.id):
                reservations.append(reservation)

    elif search_category == '2': # by 'Email' # OK
        if display_received:
            reservations = Reservation.objects.filter(user__email__contains=keywords)
        else:
            reservations = Reservation.objects.filter(user__email__contains=keywords, received=False)

    elif search_category == '3': # by 'Reservation Name'
        if display_received:
            tmp_reservations = Reservation.objects.all()
        else:
            tmp_reservations = Reservation.objects.filter(received=False)
        
        # look for ID's that contains keyword
        reservations = []
        for reservation in tmp_reservations:
            if keywords.lower() in (str(reservation.first_name) + ' ' + str(reservation.last_name)).lower():
                reservations.append(reservation)

    else:
        if display_received:
            reservations = Reservation.objects.all()
        else:
            reservations = Reservation.objects.filter(received=False)

        
    context['reservations'] = reservations
 
    return render(request, 'store/reservations_list.html', context)


def set_reservation_as_received_view(request, reservation_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('must_authenticate')
    
    reservation_object = get_object_or_404(Reservation, id=reservation_id)
    reservation_object.received = True
    reservation_object.save()

    return redirect('reservations_list')