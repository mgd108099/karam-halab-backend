from rest_framework import serializers
from .models import Customer, Product, Invoice, InvoiceItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'unit_price']

class InvoiceSerializer(serializers.ModelSerializer):
    # لجلب تفاصيل المواد داخل الفاتورة وأسماء الزبون والمندوب
    items = InvoiceItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    delegate_name = serializers.CharField(source='delegate.username', read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'customer_name', 'delegate', 'delegate_name', 'date', 'total_amount', 'items']