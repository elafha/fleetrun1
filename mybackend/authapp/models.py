# from datetime import datetime
# from uuid import uuid4
# from django.core.validators import RegexValidator
# from django.db import models
# from django.contrib.auth.models import AbstractUser

#
# def create_guid():
#     return str(uuid4())
#
#
# # ------------------------
#
#
# # User Model // the main models of all types of users
# class CustomUser(AbstractUser):
#     id = models.UUIDField(primary_key=True, verbose_name='ID', default=create_guid)  # id
#     # -------------
#     # if the user forget the password he can reset it by the phone number
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list
#     # the phone number, we activate this user by its phone number
#     # -------------
#     created_at = models.DateTimeField(default=str(datetime.now()))  # the date that this user created this account


from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from uuid import uuid4


def create_guid():
    return str(uuid4())


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                               "'+999999999'. Up to 15 digits allowed.")


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Provide a unique related_name
        related_query_name='custom_user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Provide a unique related_name
        related_query_name='custom_user'
    )
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    # if the user forget the password he can reset it by the phone number
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list
    # the phone number, we activate this user by its phone number
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
