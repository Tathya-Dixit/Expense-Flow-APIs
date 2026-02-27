from django.urls import path, include
from rest_framework.routers import DefaultRouter

from expense import views

router = DefaultRouter()

router.register('categories', views.CategoryViewSet, basename='categories')
router.register('transactions', views.TransactionViewSet, basename='transactions')
router.register('budgets', views.BudgetViewSet, basename='budgets')

urlpatterns = router.urls
