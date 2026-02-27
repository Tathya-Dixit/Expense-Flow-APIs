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


class BudgetSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, required=False)
    
    class Meta:
        model = Budget
        fields = ['id','category','category_details','limit','month','year','created_at','updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_category(self, value):
        if value and (value.created_by != self.context['request'].user) and not value.is_predefined:
            raise serializers.ValidationError("Invalid Category")
        return value
    
    def validate(self, data):
        user = self.context['request'].user
        category = data.get('category', getattr(self.instance, 'category', None)) # just using data.get(category, None) will return None in case the category isn't provided in PATCH request, to avoid that we pull data directly from the instance.
        month = data.get('month', getattr(self.instance, 'month', None))
        year = data.get('year', getattr(self.instance, 'year', None))

        qs = Budget.objects.filter(created_by = user, category = category, month = month, year = year)
        
        #below 2 lines are redundant question for future me why?
        if self.instance: #instance only exists during an update not create
            qs = qs.exclude(pk = self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A budget with these details already exists.")
        return data
        
