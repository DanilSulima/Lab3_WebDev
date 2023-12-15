from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from instruments.views import (
    InstrumentsListView, InstrumentsDetailView,
    OrderListView, OrderDetailView, LoginView,
    RegisterView, UserListView, CustomAuthToken
)

schema_view = get_schema_view(
    openapi.Info(
        title="MusicStore API",
        default_version='v1',
        description="API for Music Store",
        terms_of_service="https://musicstore/policies/terms/",
        contact=openapi.Contact(email="danilggghjf@gmail.com"),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view()),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='custom_login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('instruments/', InstrumentsListView.as_view(), name='instruments-list'),
    path('instruments/<int:pk>/', InstrumentsDetailView.as_view(), name='instruments-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
