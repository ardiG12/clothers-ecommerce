from django.shortcuts import render
from rest_framework import permissions, authentication
from rest_framework.viewsets import ModelViewSet

from app import models, serializers


class User(ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]