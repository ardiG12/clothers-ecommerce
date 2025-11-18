from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    # если есть отдельные вьюхи — добавляй сюда:
    # path('example/', ExampleView.as_view(), name='example'),
]

urlpatterns += router.urls
