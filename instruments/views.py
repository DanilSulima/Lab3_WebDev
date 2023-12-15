from contextvars import Token
from django.contrib.auth import authenticate, login
from knox.models import AuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from MusicStore.permissions import IsAdmin
from .models import Instruments, Order
from .serializers import InstrumentsSerializer, OrderSerializer, RegistrationSerializer, UserDetailSerializer
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class YourView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Використовуйте обидві перевірки

    def get(self, request):
        # Ваш код для GET запиту
        return Response({"message": "You have access!"})

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])

        if user:
            _, token = AuthToken.objects.create(user)
            return Response({'token': token})
        else:
            return Response({'detail': 'Invalid credentials'}, status=401)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework import status

class UserListView(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserDetailSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

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

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
