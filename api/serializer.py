from rest_framework import serializers
from .models import User, Contact, SpamReport

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'password']
        extra_kwargs = { 'password': { 'write_only': True } }

    def create(self, validArgs):
        user = User.objects.create_user(**validArgs)
        return user
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [ 'id', 'name', 'phone_number', 'email' ]

class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = [ 'id', 'reported_user', 'phone_number', 'is_spam' ]

