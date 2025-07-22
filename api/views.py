from rest_framework import generics
from .serializers import RegisterSerializer,BookSerializer,RentalSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, permissions
from .models import Book,Rental
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User  


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admin can see all rentals
        if self.request.user.is_staff:
            return Rental.objects.all()
        # Regular users can only see their own rentals
        return Rental.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate rental with logged-in user
        serializer.save(user=self.request.user)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def perform_create(self, serializer):
        # Associate rental with logged-in user
        serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer