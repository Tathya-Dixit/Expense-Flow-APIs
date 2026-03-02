from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone

import logging

from expense.serializers import CategorySerializer, TransactionSerializer, BudgetSerializer
from expense.models import Category, Transaction, Budget
from expense.filters import TransactionFilter

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    filterset_fields = ['type_choice', 'is_predefined']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        return Category.objects.filter(Q(created_by = self.request.user) | Q(is_predefined = True))
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_predefined :
            return Response({"message" : "can not edit predefined categories"}, status=status.HTTP_403_FORBIDDEN)
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_predefined :
            return Response({"message" : "can not delete predefined categories"}, status=status.HTTP_403_FORBIDDEN)
        
        return super().destroy(request, *args, **kwargs)

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



class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    search_fields = ['description']
    ordering_fields = ['transaction_date']
    ordering = ['transaction_date']

    def get_queryset(self):
        return Transaction.objects.filter(Q(created_by = self.request.user) & Q(is_deleted = False))
    
    def perform_create(self, serializer):
        logger.info(f"User - {self.request.user} creating transaction")
        serializer.save(created_by = self.request.user)
        logger.info(f"Transaction created Tn-ID: {serializer.instance.id}")
    
    def perform_update(self, serializer):
        logger.info(f"Updating transaction Tn-ID: {serializer.instance.id}")
        serializer.save()
        logger.info(f"Transaction updated Tn-ID: {serializer.instance.id}")
    
    def perform_destroy(self, instance):
        logger.info(f"Deleting transaction Tn-ID: {instance.id}")
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()
        logger.info(f"Transaction deleted Tn-ID: {instance.id}")
    


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    filterset_fields = ['month', 'year', 'category']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    
    def get_queryset(self):
        return Budget.objects.filter(created_by = self.request.user)
    
    def perform_create(self, serializer):
        logger.info(f"User - {self.request.user} creating budget")
        instance = serializer.save(created_by = self.request.user)
        logger.info(f"Budget created : \n[user : {instance.created_by}, category : {instance.category}, month : {instance.month}, year : {instance.year}]")
    
    def perform_update(self, serializer):
        instance = serializer.instance
        logger.info(f"Updating Budget: \n[user : {instance.created_by}, category : {instance.category}, month : {instance.month}, year : {instance.year}]")
        instance = serializer.save()
        logger.info(f"Budget Updated: \n[user : {instance.created_by}, category : {instance.category}, month : {instance.month}, year : {instance.year}]")
    
    def perform_destroy(self, instance):
        logger.info(f"Deleting Budget: \n[user : {instance.created_by}, category : {instance.category}, month : {instance.month}, year : {instance.year}]")
        instance.delete()
        logger.info(f"Budget Delete: \n[user : {instance.created_by}, category : {instance.category}, month : {instance.month}, year : {instance.year}]")
