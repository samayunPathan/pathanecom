from django.shortcuts import render
from store.models import Product

# Create your views here.

def font_page(request):
    products=Product.objects.filter(status=Product.ACTIVE)[:12]
    return render(request,'core_app/fontpage.html',{'products':products})

def about(request):
    return render(request,'core_app/about.html')

