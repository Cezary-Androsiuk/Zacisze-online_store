from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from hashid_field import HashidAutoField

from account.models import (
    Account
)


def upload_location(instance, filename, **kwargs):
    file_path = 'store/{title}/{filename}'.format(
        title=slugify(instance.title), filename=filename
    )
    return file_path

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.CharField(max_length=5000, null=False, blank=True, default='')
    
    authors = models.CharField(max_length=200, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location)

    price = models.FloatField(null=False, blank=False)
    added_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    is_deleted = models.BooleanField(null=False, blank=True, default=False)
    containsNotConfirmedComments = models.PositiveIntegerField(null=False, blank=True, default=0)
    
    def __str__(self):
        return f'ID: {str(self.product_id)},  TITLE: "{self.title}", ADDED_BY: {self.added_by.email}'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
    
# prevent keeping the image after the post was deleted
@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

# execute action before it was saved
def pre_save_product_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_product_receiever, sender=Product)







class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, blank=False)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f'ID: {self.id},  USER: {self.user.email}'
    
    @property
    def get_cart_total(self):
        # btw dir(self) helped to solve 'self do not have orderitem_set parameter' by printing all 
        # parameters afer self.*something* and by removing values that was in both sets i found 
        # that I should use cartitem_set istead of orderitem_set, but still i don't know where it come from...
        cartitems = self.cartitem_set.all()
        total = sum([item.get_total for item in cartitems])
        return total
    
    @property
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

    def create_order(self, order_data):
        print('in create...')
        order = Order.objects.create(
            user=self.user,
            **order_data
        )
        
        for cart_item in self.cartitem_set.all():
            print('\tcreating OrderItem...')
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            order_item.save()
            print('\t...OrderItem created!', order_item)
            print()
        print('...created!')
        return order
    
    
    def create_reservation(self, reservation_data):
        print('in create...')
        reservation = Reservation.objects.create(
            user=self.user,
            **reservation_data
        )
        
        for cart_item in self.cartitem_set.all():
            print('\tcreating ReservationItem...')
            reservation_item = ReservationItem.objects.create(
                reservation=reservation,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            reservation_item.save()
            print('\t...OrderItem created!', reservation_item)
            print()
        print('...created!')
        return reservation
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'CART ID: {self.cart.id},  USER: {self.cart.user.email},  PRODUCT: {self.product.product_id},  Quantity: {self.quantity}'
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    










class Order(models.Model):
    id = HashidAutoField(primary_key=True, min_length=16, salt="OrderSalt_skhjfks")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, blank=False)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)

    
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=400, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    city = models.CharField(max_length=200, null=False, blank=False)
    zip_code = models.CharField(max_length=6, null=False, blank=False)

    card_name = models.CharField(max_length=400, null=False, blank=False)
    card_id = models.CharField(max_length=19, null=False, blank=False)
    card_exp = models.CharField(max_length=5, null=False, blank=False)
    card_cvv = models.CharField(max_length=3, null=False, blank=False)

    delivered = models.BooleanField(null=False, blank=True, default=False)

    def __str__(self):
        # return f'ID: {str(self.id)[-4:]},  USER: {self.user.email},  STATUS: {"finished" if self.delivered else "in shipment"}'
        return f'ID: {self.id},  USER: {self.user.email},  STATUS: {"finished" if self.delivered else "in shipment"}'

    def set_to_delivered(self):
        self.delivered = True
        
    @property
    def get_order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        # return f'ID: {str(self.order.id)[-4:]},  USER: {self.order.user.email},  PRODUCT: {self.product.product_id},  Quantity: {self.quantity}'
        return f'ORDER ID: {self.order.id},  USER: {self.order.user.email},  PRODUCT: {self.product.product_id},  Quantity: {self.quantity}'
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    








class Reservation(models.Model):
    id = HashidAutoField(primary_key=True, min_length=16, salt="ReservationSalt_fjhgikds")
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False, blank=False)
    products = models.ManyToManyField(Product, through='ReservationItem')
    reservation_date = models.DateTimeField(auto_now_add=True)
    
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=400, null=False, blank=False)
    country = models.CharField(max_length=200, null=False, blank=False)
    city = models.CharField(max_length=200, null=False, blank=False)
    zip_code = models.CharField(max_length=6, null=False, blank=False)

    received = models.BooleanField(null=False, blank=True, default=False)

    def __str__(self):
        # return f'ID: {str(self.id)[-4:]},  USER: {self.user.email},  STATUS: {"recived" if self.received else "waiting"}'
        return f'ID: {self.id},  USER: {self.user.email},  STATUS: {"recived" if self.received else "waiting"}'

    def set_to_received(self):
        self.received = True
        
    @property
    def get_reservation_total(self):
        reservation_items = self.reservationitem_set.all()
        total = sum([item.get_total for item in reservation_items])
        return total

        
class ReservationItem(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        # return f'ID: {str(self.reservation.id)[-4:]},  USER: {self.reservation.user.email},  PRODUCT: {self.product.product_id},  Quantity: {self.quantity}'
        return f'RESERVATION ID: {self.reservation.id},  USER: {self.reservation.user.email},  PRODUCT: {self.product.product_id},  Quantity: {self.quantity}'
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total



class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    content = models.TextField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'target {self.product} by {self.user}'

class Reply(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='replies', null=False, blank=False)
    parentComment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', null=False, blank=False)
    content = models.TextField()

    def __str__(self):
        return f'target {self.parentComment} by {self.user}'
    