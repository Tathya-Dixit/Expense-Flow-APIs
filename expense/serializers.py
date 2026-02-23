from rest_framework import serializers

from expense.models import Category, Transaction, Budget


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']
