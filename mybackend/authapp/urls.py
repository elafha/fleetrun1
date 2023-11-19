from django.urls import path
# from .views import UserLoginViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewset, GroupViewset, PermissionViewset

urlpatterns = [
    # path('create_user', CreateUserView.as_view(), name='create_user'),
    path('token', TokenObtainPairView.as_view(), name='access_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login_v1', UserLoginViewSet.as_view({'get': 'list', 'post': 'create'}, ), name='login'),

    path('user', UserViewset.as_view({'get': 'list'}), name='user'),
    path('user/<int:pk>', UserViewset.as_view({'get': 'retrieve'}), name='user'),
    path('group', GroupViewset.as_view({'get': 'list'}), name='group'),
    path('group/<int:pk>', GroupViewset.as_view({'get': 'retrieve'}), name='group'),
    path('permission', PermissionViewset.as_view({'get': 'list'}), name='permission'),
    path('permission/<int:pk>', PermissionViewset.as_view({'get': 'retrieve'}), name='permission'),
]
