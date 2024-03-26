from django.urls import path
from core_app import views
from django.conf import settings
from django.contrib.staticfiles.urls import static ,staticfiles_urlpatterns

app_name='core_app'

urlpatterns = [
    path('',views.font_page,name='font_page'),
    path('about/',views.about,name='about'),
]


urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

