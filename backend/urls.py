from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # روابط تطبيق المحمصة
    path('api/', include('core.urls')), 
    
    # الرابط الخاص بتسجيل دخول المندوب من الموبايل
    path('api/login/', obtain_auth_token), 
]