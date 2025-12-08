from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from app.filter import ProductFilter
from app.pagination import Pagination
from app.permissions import IsAdminOrReadOnly
from app.serializers import *
from app.models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class CartViewSet(ModelViewSet):
    serializer_class = CartProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CartProduct.objects.none()
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    @action(detail=False, methods=["post"])
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)

        item, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
        )

        if not created:
            item.quantity += quantity
        item.save()

        return Response({"message": "Товар добавлен!"}, status=201)
