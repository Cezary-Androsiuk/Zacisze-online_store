from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path('', store_view, name='store'),
    path('create_product/', create_product_view, name='create_product'),
    path('<slug>/', view_product_view, name='view_product'),
    path('<slug>/edit', edit_product_view, name='edit_product'),
    path('<slug>/add_comment', add_comment_view, name='add_comment'),
    path("<int:comment_id>/confirm_comment/", confirm_comment_view, name='confirm_comment'),
    path("<int:comment_id>/add_reply/", add_reply_view, name='add_reply'),
    path("<slug>/delete", delete_product_view, name='delete_product'),
    path('<slug>/delete_product_confirmed', delete_product_confirmed_view, name='delete_product_confirmed'),
    path("<slug>/add_to_cart/", add_to_cart_view, name='add_to_cart'),
    path("<slug>/rm_from_cart/", rm_from_cart_view, name='rm_from_cart'),
    path("<slug>/rm_cart_item/", rm_cart_item_view, name='rm_cart_item'),
]