from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from django.db.models import Q
from .models import Contact
from .serializers import ContactSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @action(detail=False, methods=['post'])
    def mark_spam(self, request):
        phone_number = request.data.get('phone_number')
        contact, created = Contact.objects.get_or_create(phone_number=phone_number)
        contact.mark_as_spam()
        return Response({'message': 'Number marked as spam'}, status=status.HTTP_200_OK)

# Search by Name
@api_view(['GET'])
def search_by_name(request):
    query = request.query_params.get('query', '').lower()
    if not query:
        return Response({"error": "No search query provided."}, status=400)

    contacts = Contact.objects.filter(Q(name__istartswith=query) | Q(name__icontains=query)).order_by('name')
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)

# Search by Phone Number
@api_view(['GET'])
def search_by_phone(request):
    phone_number = request.query_params.get('phone_number')
    if not phone_number:
        return Response({"error": "No phone number provided."}, status=400)

    contacts = Contact.objects.filter(phone_number=phone_number)
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)
