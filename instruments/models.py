from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers


class CustomUser(AbstractUser):
    def authenticate_user(self, username, password):
        user = authenticate(username=username, password=password)
        db_table = 'Users'
        return user
    pass


class Instruments(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    instruments = models.ForeignKey(Instruments, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    costumer_name = models.CharField(max_length=255)
    costumer_email = models.EmailField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order for {self.instruments.name} by {self.costumer_name}'
class InstrumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instruments
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
