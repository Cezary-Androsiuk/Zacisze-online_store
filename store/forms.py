from django import forms

from store.models import (
    Product,
    Order,
    Reservation
)

class CreateProductForm(forms.ModelForm):

    # how form should look like
    class Meta:
        model = Product
        # fields that user are able to setup while filling the form
        fields = ['title', 'authors', 'description', 'image', 'price']

        
class UpdateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['title', 'authors', 'description', 'image', 'price']

    def save(self, commit=True):
        product = self.instance
        product.title = self.cleaned_data['title']
        product.authors = self.cleaned_data['authors']
        product.description = self.cleaned_data['description']
        product.price = self.cleaned_data['price']

        if self.cleaned_data['image']:
            product.image = self.cleaned_data['image']

        if commit:
            product.save()
        return product
        


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'country', 'city', 'zip_code', 'card_name', 'card_id', 'card_exp', 'card_cvv']


class ReservationForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = ['first_name', 'last_name', 'address', 'country', 'city', 'zip_code']
