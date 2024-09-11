from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, search_by_name, search_by_phone

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('name', search_by_name),
    path('phone', search_by_phone),
]
