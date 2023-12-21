from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings

from account.forms import (
    RegistrationForm, 
    AccountAuthenticationForm,
    AccountUpdateForm
)

from account.models import (
    Account,
)

from store.models import (
    Cart,
    CartItem,
    Order,
    Reservation,
)

def create_cart(email):
    print('given email for creating a cart:', email)
    # get user that have given email
    user = Account.objects.filter(email=email).first()
    print('creating cart for', user, 'user')
    # get cart associated with current user
    user_cart = Cart.objects.filter(user=user).first()
    # if user do not have cart associated then
    #   create new cart for hom
    if not user_cart:
        user_cart = Cart(user=user)
        user_cart.save()
        print('cart created for', user, 'user')
    pass

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            print('User Registered!')
            # if is registered then create cart for him
            create_cart(email)
            return redirect('home')
        
    else:
        form = RegistrationForm()
    
    context['debug_mode'] = settings.DEBUG
    context['registration_form'] = form
    context['registered_accounts'] = Account.objects.all()
    return render(request, 'account/register.html', context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    # return redirect(request.META['HTTP_REFERER']) # return to the same page
    return redirect('home')

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect(request.META['HTTP_REFERER']) # return to the same page

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                # just for safe, do not request rebuild database
                # adds cart for users that do not have it 
                create_cart(email) 
                return redirect('home')
    else:
        form = AccountAuthenticationForm()

    context['debug_mode'] = settings.DEBUG
    context['login_form'] = form
    context['registered_accounts'] = Account.objects.all()
    return render(request, 'account/login.html', context)



def account_view(request):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email" :request.POST['email'],
                "username" :request.POST['username'],
            }
            form.save()
            context['success_message'] = 'Updated'
            return render(request, 'account/account.html', context)
    else:
        # displayed values ass soon user visited page 
        form = AccountUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username
            }
        )
    context['account_form'] = form

    orders=Order.objects.filter(user=request.user)
    reservations=Reservation.objects.filter(user=request.user)
    context['orders'] = orders
    context['reservations'] = reservations

    return render(request, 'account/account.html', context)

def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
