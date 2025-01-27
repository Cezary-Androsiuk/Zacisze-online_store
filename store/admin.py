from django.contrib import admin
from store.models import *

admin.site.register(Product)

admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Reservation)
admin.site.register(ReservationItem)

admin.site.register(Comment)
admin.site.register(Reply)