from app import models
from app.models import User, Profile
from rest_framework import serializers
from app.models import Cart, CartProduct, Product

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        exclude = ("user", "reset_code")
        read_only_fields = ("id",)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = "__all__"
        read_only_fields = ("id",)

    def get_discount(self, obj):
        if obj.old_price and obj.old_price > obj.price:
            return float(obj.old_price - obj.price)

        return 0

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        Profile.objects.create(user=user)

        user.set_password(validated_data['password'])
        return user

class CartProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="product.title", read_only=True)
    price = serializers.DecimalField(source="product.price", read_only=True,
                                     max_digits=10, decimal_places=2)
    image = serializers.ImageField(source="product.image", read_only=True)

    class Meta:
        model = models.CartProduct
        fields = ["id", "title", "price", "quantity", "image"]


class AddToCartSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField(default=1)


class RemoveCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(required=False, min_value=1)

    def save(self, **kwargs):
        user = self.context["user"]
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError({"message": "Корзина не найдена"})

        product_id = int(self.validated_data["product_id"])  # ⚡ приводим к int

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"message": "Товар не найден"})

        try:
            item = CartProduct.objects.get(id=product_id, cart=cart)  # ⚡ ищем по product__id
        except CartProduct.DoesNotExist:
            raise serializers.ValidationError({"message": "Товара нет в корзине"})

        quantity = self.validated_data.get("quantity")
        if quantity:
            if item.quantity > quantity:
                item.quantity -= quantity
                item.save()
            else:
                item.delete()
        else:
            item.delete()

        return cart