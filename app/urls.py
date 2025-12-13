from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'products', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'cart', CartViewSet,basename='cart')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/veriy/', TokenVerifyView.as_view(), name='token_verify'),

    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
