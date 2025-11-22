from rest_framework import serializers

from app import models


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
