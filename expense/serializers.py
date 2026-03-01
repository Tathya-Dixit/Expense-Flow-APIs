from rest_framework import serializers
from django.db.models import Q

from expense.models import Category, Transaction, Budget, Type


class CategorySerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Type.choices, source='type_choice', default=Type.EXPENSE) # type here won't conflict with the type method but it would have conflicted if used in models while calling the instance.type

    class Meta:
        model = Category
        fields =['id', 'name', 'type', 'description', 'created_at']
        read_only_fields = ['created_at']


class TransactionSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none(), write_only=True, required=False)
    type = serializers.ChoiceField(choices=Type.choices, source='type_choice', default = Type.EXPENSE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['category'].queryset = Category.objects.filter(Q(created_by = request.user) | Q(is_predefined = True)) # this way invalid category will be rejected at the field lever no need to validate

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type', 'description', 'payment_method', 'category_details', 'category', 'transaction_date', 'created_at']
        read_only_fields = ['created_at']
    
    def validate(self, data):
        category = data.get('category')
        type_choice = data.get('type_choice')

        if category and type_choice and category.type_choice != type_choice:
            raise serializers.ValidationError('Transaction type must match category type')
        return data
    


class BudgetSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none(), write_only=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['category'].queryset = Category.objects.filter(Q(created_by = request.user) | Q(is_predefined = True)) # this way invalid category will be rejected at the field lever no need to validate
    
    class Meta:
        model = Budget
        fields = ['id','category','category_details','limit','month','year','created_at','updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    
    def validate(self, data):
        user = self.context.get('request').user
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
        
