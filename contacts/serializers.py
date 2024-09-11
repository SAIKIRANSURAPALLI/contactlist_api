from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    owner_email = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'is_spam', 'spam_likelihood', 'owner_email']

    def get_owner_email(self, obj):
        request_user = self.context.get('request').user  
        owner = obj.owner  
        if request_user in owner.contacts.all(): 
            return owner.email
        return None  
