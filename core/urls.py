from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ProductViewSet, InvoiceViewSet, login_view # ✨ استدعينا الدالة الجديدة

# Router يقوم بتوليد الروابط الأساسية تلقائياً
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    # ✨ ضفنا مسار تسجيل الدخول المخصص لحتى يبعت الأسماء والأرقام
    path('login/', login_view, name='login'),
    
    path('', include(router.urls)),
]