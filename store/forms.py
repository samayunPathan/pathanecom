from django import forms
from .models import Product,Order,OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
       
        model=Order
        fields=('first_name','last_name','email','address','zipcode','phone',)
        widgets={
            'first_name':forms.TextInput( attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'last_name':forms.TextInput(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'email':forms.EmailInput(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'address':forms.Textarea(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'zipcode':forms.NumberInput(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'phone':forms.NumberInput(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
        }

class ProductForm(forms.ModelForm):
    
    class Meta:
        model=Product
        fields = ("category","title","description","price","image",)
        widgets={
            'category':forms.Select(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'title':forms.TextInput(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'description':forms.Textarea(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'price':forms.TextInput(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
            'image':forms.FileInput(attrs={
                'class':'w-full p-4 border border-gray-200'
            }),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Marking fields as required
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].required = True
            self.fields['address'].required = True
            self.fields['zipcode'].required = True
            self.fields['phone'].required = True
