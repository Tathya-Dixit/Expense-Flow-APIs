import django_filters

from expense.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    amount_min = django_filters.NumberFilter('amount', lookup_expr='gte')
    amount_max = django_filters.NumberFilter('amount', lookup_expr='lte')
    date_from = django_filters.DateFilter('transaction_date', lookup_expr='gte')
    date_to = django_filters.DateFilter('transaction_date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['type_choice', 'payment_method', 'category', 'amount_min', 'amount_max', 'date_from', 'date_to']
