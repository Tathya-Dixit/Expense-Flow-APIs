from rest_framework import serializers

from expense.models import Category, Transaction, Budget


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class TransactionSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, required=False)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type_choice', 'description', 'payment_method', 'category_details', 'category', 'transaction_date', 'created_at']
        read_only_fields = ['created_at']
    
    def validate_category(self, value):
        if value and (value.created_by != self.context['request'].user) and not value.is_predefined:
            raise serializers.ValidationError("Invalid Category")
        return value