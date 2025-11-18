from django.shortcuts import render
from rest_framework import permissions, authentication
from rest_framework.viewsets import ModelViewSet

from app.serializers import *
from app.models import *

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer