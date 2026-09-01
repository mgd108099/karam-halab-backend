from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .models import Customer, Product, Invoice
from .serializers import CustomerSerializer, ProductSerializer, InvoiceSerializer

# --- دالة تسجيل الدخول المخصصة ---
@api_view(['POST'])
@permission_classes([AllowAny]) # السماح للجميع بمحاولة الدخول
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # التحقق من صحة بيانات المندوب
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # إنشاء أو جلب الرمز السري (Token)
        token, created = Token.objects.get_or_create(user=user)
        
        # جلب بيانات الطباعة من جدول DelegateProfile
        try:
            profile = user.profile
            print_names = profile.print_names if profile.print_names else "موالح كرم حلب"
            print_phones = profile.print_phones if profile.print_phones else ""
        except:
            # قيم افتراضية في حال لم يكن للمندوب ملف إضافي
            print_names = "موالح كرم حلب"
            print_phones = ""
            
        return Response({
            'token': token.key,
            'print_names': print_names,
            'print_phones': print_phones
        }, status=200)
    else:
        return Response({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}, status=400)


# --- باقي الكود الأساسي الخاص بك ---
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated] # حماية: يتطلب تسجيل دخول

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    # حفظ المندوب (المستخدم الحالي) تلقائياً عند إنشاء فاتورة جديدة
    def perform_create(self, serializer):
        serializer.save(delegate=self.request.user)