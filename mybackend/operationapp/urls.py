from django.urls import path
# from rest_framework import routers

from .views import DriverViewSet

# router = routers.DefaultRouter()
# router.register(r'driver', DriverViewSet)
#
urlpatterns = [
    # path('driver', include(router.urls))
    path('driver', DriverViewSet.as_view({'get': 'list', 'post': 'create'}, name='driver-list-create')),
]
