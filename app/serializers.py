from rest_framework import serializers

from app import models
from app.models import User, Profile


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
    class Meta:
        model = models.Product
        fields = "__all__"


class AddToCartSerializer(serializers.Serializer):
        product_id = serializers.IntegerField()
        quantity = serializers.IntegerField(default=1)