from django.urls import path, include
from rest_framework.routers import DefaultRouter

from expense import views

router = DefaultRouter()

router.register('categories', views.CategoryViewSet, basename='categories')

urlpatterns = router.urls
