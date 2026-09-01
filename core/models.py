from django.db import models
from django.contrib.auth.models import User

# 1. جدول الزبائن
class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم الزبون")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم الهاتف")
    address = models.TextField(blank=True, null=True, verbose_name="العنوان")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 2. جدول المواد (المنتجات)
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="اسم المادة")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    stock = models.IntegerField(default=0, verbose_name="الكمية المتوفرة")
    
    # ✨ الحقل الجديد: الحد الأدنى للتنبيه
    min_limit = models.IntegerField(default=5, verbose_name="الحد الأدنى للتنبيه")

    def __str__(self):
        return self.name

# 3. جدول الفاتورة الأساسي
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices', verbose_name="الزبون")
    delegate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المندوب")
    date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الفاتورة")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="المجموع الكلي")
    
    def __str__(self):
        return f"فاتورة رقم {self.id} - {self.customer.name}"

# 4. جدول تفاصيل الفاتورة (المواد داخل الفاتورة)
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(verbose_name="الكمية")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الإفرادي")

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

# 5. جدول تفاصيل المندوب الإضافية (Profile)
class DelegateProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'مدير النظام'),
        ('delegate', 'مندوب مبيعات'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="حساب المندوب")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='delegate', verbose_name="الصلاحية")
    
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="رقم جوال النظام الداخلي")
    print_names = models.CharField(max_length=255, blank=True, null=True, verbose_name="الأسماء المطبوعة على الفاتورة")
    print_phones = models.CharField(max_length=255, blank=True, null=True, verbose_name="الأرقام المطبوعة على الفاتورة")

    def __str__(self):
        return f"ملف المندوب: {self.user.username}"