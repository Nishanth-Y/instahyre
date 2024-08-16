from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Contact, SpamReport
from .serializer import *
user = get_user_model()
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny]
        return super().get_permissions()

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.contacts.all()
    

class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=['post'])
    def mark_spam(self, request):
        phone_number = request.data.get('phone_number')
        report, created = SpamReport.objects.get_or_create(reported_user = request.user, phone_number = phone_number, is_spam = True)
        return Response({'Status': 'Marked As Spam'})
    
    @action(detail=False, methods=['post'])
    def search_by_number(self, request):
        phone_number = request.query_params.get('phone_number')
        results = Contact.objects.filter(phone_number=phone_number)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def search_by_name(self, request):
        name = request.query_params.get('name')
        results = Contact.objects.filter(name__icontains=name)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
    
    