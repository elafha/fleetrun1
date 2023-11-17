from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('operationapp.urls')),
    path('api/v1/', include('authapp.urls')),
    # path('api/v1/auth/', include('authapp.urls')),
]
