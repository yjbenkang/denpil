from rest_framework import serializers
from .models import BookSalesInfo, PublisherSalesData

class BookSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSalesInfo
        fields = ['discount_rate', 'sales_point']  # 필요한 필드만 선택

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublisherSalesData
        fields = ['publisher', 'total_sales', 'book_count']  # 필요한 필드만 선택