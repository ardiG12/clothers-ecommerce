from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'products', ProductViewSet)
router.register(r'category', CategoryViewSet)
urlpatterns = [
]

urlpatterns += router.urls
