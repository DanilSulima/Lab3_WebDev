# serializers.py
from .models import Instruments, Order, CustomUser
from rest_framework import serializers
from django.contrib.auth.models import User

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

class InstrumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruments
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_email(self, value):

        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Неправильний формат електронної пошти.")

        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ім'я користувача вже використовується.")

        return value
