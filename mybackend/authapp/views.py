from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group, Permission
from rest_framework import status, viewsets, permissions
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer, UserLoginSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .models import CustomUser

# class CreateUserView(viewsets.ModelViewSet):
#
#     def create(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         if not username or not password:
#             return Response({'message': 'Both username and password are required'}, status=status.HTTP_BAD_REQUEST)
#
#         # Check if the user already exists
#         if User.objects.filter(username=username).exists():
#             return Response({'message': 'User with this username already exists'}, status=status.HTTP_BAD_REQUEST)
#
#         # Create the user
#         user = User.objects.create_user(username, password=password)
#
#         # Generate JWT token
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#
#         return Response({'message': 'User created', 'access_token': access_token}, status=status.HTTP_201_CREATED)

#
# class UserLoginViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserLoginSerializer
#     permission_classes = [permissions.AllowAny]
#
#     def create(self, request, *args, **kwargs):
#         serializer = request.data
#         print(serializer)
#         username = serializer.get('username')
#         password = serializer.get('password')
#
#         if not username or not password:
#             return Response({"msg": "Both username and password are required", "status": False})
#
#         print(serializer)
#         user = CustomUser.objects.get(username=username, password=password)
#         print("user", user)
#
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return JsonResponse({'access_token': token.key, "status": True})
#         elif Exception:
#             return Response({"msg": "Invalid credentials", "status": False})
#         return Response(serializer.errors, status=False)
# #
#     def list(self, request, *args, **kwargs):
#         return JsonResponse({'name': 'elaf'})

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     return Response({'name': 'elaf'})


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PermissionViewset(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

