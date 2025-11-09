from rest_framework import serializers

from app import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        exclude = ("user","reset_code")
        read_only_fields = ("id",)