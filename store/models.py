from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image

# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)


    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.title

class Product(models.Model):
    DRAFT ='draft'
    WAITING_APPROVAL='waitingapproval'
    ACTIVE='active'
    DELETED='deleted'

    STATUS_CHOICES=(
        (DRAFT ,'Draft'),
        (WAITING_APPROVAL,'Waiting approval'),
        (ACTIVE,'Active'),
        (DELETED,'Deleted'),

    )

    user=models.ForeignKey(User,related_name='products',on_delete=models.CASCADE)
    category=models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)
    description=models.TextField(blank=True)
    price=models.IntegerField()
    image=models.ImageField(upload_to='uploads/product_images',blank=True,null=True)
    thumbnail=models.ImageField(upload_to='uploads/product_images/thumbnail',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default=ACTIVE)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return self.title
    def get_price(self):
        return self.price
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'

    
        
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85) 
        name=image.name.replace('uploads/product_images/','')
        thumbnail = File(thumb_io, name=name)

        return thumbnail
class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent=models.CharField(max_length=255,blank=True,null=True)

    is_paid = models.BooleanField(default=False,blank=True)
    paid_amount = models.IntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ('-created_at',)
    
    def get_total_price(self):
        if self.paid_amount:
            return self.paid_amount 
        
        return 0
    
    
    def get_products(self):
        
        return list(self.items.values_list('product__title', flat=True))[0]
    
    def get_quantity(self):
        products = self.items.values_list('product__title', 'quantity')
        return list(products)[0][1]

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.price 
    