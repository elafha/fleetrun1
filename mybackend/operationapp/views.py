from uuid import uuid4

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Driver, CustomUser
from .serializers import DriverSerializer


from twilio.rest import Client
from django.http import HttpResponse
from django.conf import settings

twilio_phone_number = settings.TWILIO_PHONE_NUMBER


def send_sms(to_number):
    TWILIO_AUTH_TOKEN = 'ba17441a5574bca578c24e6f81a2851f'
    TWILIO_ACCOUNT_SID = 'AC691181008e76d860f6d497317b5b880a'

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        to='+905355561712'
    )

    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # to_number = to_number  # Replace with the recipient's phone number
    # message = client.messages.create(
    #     body="Hello from your Django app!",
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=to_number
    return HttpResponse(f"SMS sent to {to_number}. SID: {message.sid}")


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = request.data
            print(serializer)

            firstname = serializer.get('firstname')
            lastname = serializer.get('lastname')
            email = serializer.get('email')
            username = serializer.get('username')
            password = serializer.get('password')
            phone_number = serializer.get('phone_number')
            is_freelance = serializer['is_freelance']
            # Query the database to check if the username exists

            try:
                user_obj = CustomUser.objects.get(username=username)
                user_id = user_obj.id
            except:
                new_user = CustomUser(username=username, password=password, first_name=firstname,
                                      last_name=lastname, is_superuser=False, email=email, phone_number=phone_number)
                new_user.save()
                print("2:", new_user)
                user_id = new_user.id
                User.objects.create_user(username=username, password=password, first_name=firstname,
                                      last_name=lastname, is_superuser=False, email=email)

            driver_obj = Driver.objects.filter(user_id=user_id).exists()
            if not driver_obj:
                new_driver = Driver(is_freelance=is_freelance, user_id=user_id)
                new_driver.save()
            else:
                return Response(
                    {"msg": "The driver already exists.", "username": username, "status": True})

            # send_sms(phone_number)
            return Response({"msg": "The driver has been added successfully.", "username": username, "status": True})
        except Exception as e:
            return Response({"msg": "Error in adding driver", "status": False, "exception": str(e)})

    def list(self, request):
        return Response({"elaf": "Tamamladı"})

