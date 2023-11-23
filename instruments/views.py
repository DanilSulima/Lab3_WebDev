from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Instruments, Order
from .serializers import InstrumentsSerializer, OrderSerializer

class InstrumentsListView(APIView):
    def get(self, request):
        instruments = Instruments.objects.all()
        serializer = InstrumentsSerializer(instruments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InstrumentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InstrumentsDetailView(APIView):
    def get_object(self, pk):
        try:
            return Instruments.objects.get(pk=pk)
        except Instruments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        instrument = self.get_object(pk)
        serializer = InstrumentsSerializer(instrument)
        return Response(serializer.data)

    def put(self, request, pk):
        instrument = self.get_object(pk)
        serializer = InstrumentsSerializer(instrument, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instrument = self.get_object(pk)
        instrument.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
