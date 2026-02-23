from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q

import logging

from expense.serializers import CategorySerializer
from expense.models import Category

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(Q(created_by = self.request.user) | Q(is_predefined = True))
    
    def perform_create(self, serializer):
        logger.info(f"User - {self.request.user} creating category")
        serializer.save(created_by = self.request.user)
        logger.info(f"Category created : {serializer.instance.name}")
    
    def perform_update(self, serializer):
        logger.info(f"Updating category: {serializer.instance.name}")
        serializer.save()
        logger.info(f"Category updated: {serializer.instance.name}")
    
    def perform_destroy(self, instance):
        logger.info(f"Deleting category: {instance.name}")
        instance.delete()
        logger.info(f"Category deleted: {instance.name}")

