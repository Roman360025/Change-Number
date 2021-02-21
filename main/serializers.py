from rest_framework import serializers

from .models import Number


class NumberListSerializer(serializers.ModelSerializer):
    """"Число в БД"""

    class Meta:
        model = Number
        fields = "__all__"


class NumberChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = "__all__"
