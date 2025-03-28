# shop/serializers.py
from rest_framework import serializers
from .models import Category, Product, Order, ComponentOption

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ComponentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentOption
        fields = ['id', 'name', 'price', 'volume']

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, allow_null=True)
    model_3d = serializers.FileField(use_url=True, allow_null=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    compatible_with = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all(), required=False)
    components = ComponentOptionSerializer(many=True, read_only=True)
    brand = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'base_price', 'description', 'image', 'model_3d', 'stock', 'discount', 'component_type', 'components', 'compatible_with', 'brand']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'