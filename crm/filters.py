
import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    email_icontains = django_filters.CharFilter(field_name='email',lookup_expr='icontains')
    phone_icontains = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'created_at']
        

class ProductFilter(django_filters.FilterSet):
    name_icontains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    stock_gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    order_by = django_filters.OrderingFilter(fields=('stock', 'stock'))

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']
        

class OrderFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name = django_filters.CharFilter(field_name='products__name', lookup_expr='icontains')
    order_date_gte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='gte')
    order_date_lte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['customer', 'products', 'order_date']