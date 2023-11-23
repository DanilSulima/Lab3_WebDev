# serializers.py
from rest_framework import serializers
from .models import Instruments, Order


class InstrumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruments
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
