from authapp.models import CustomUser
from django.db import models
from uuid import uuid4


# creating a default str id for each model based on uuid instead of serial number
def create_guid():
    return str(uuid4())


class Customer(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    name = models.CharField(max_length=255)  # the name of the customer if exists
    number = models.IntegerField()  # customer's phone number

    def __str__(self):
        return self.name


class Address(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    name = models.CharField(max_length=50)  # the address place: home, work, university, school, or something else
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    # --------------- we can send the (longitude+latitude) at least if the map link doesn't exist --------------- #
    longitude = models.IntegerField()  # the longitude of the address # it should be a number
    latitude = models.IntegerField()  # the latitude of the address  # it should be a number
    map_link = models.TextField(verbose_name="map")  # the link of the map to make it easier for navigation

    def __str__(self):
        return self.map_link


class Agent(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    # the link of the image that already stored (the logo of the agent's company)
    image = models.TextField()
    # the agent should have a user in our records
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    # the address of our agent
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    # is this agent a main branch or sub branch
    is_main_branch = models.BooleanField()


class Driver(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    image = models.TextField()  # the link to driver's image in our storage (its optional)
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)  # the driver has a user in our records
    # we have a drivers are working as an employee in our company, whereas the part-time job is available too
    is_freelance = models.BooleanField()
    # # the user who added this driver to our records | hint: it could be a super admin,
    # # or any member has the permission to add a driver
    # added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Order(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    added_at = models.DateTimeField()  # the datetime of creating this order
    # who add this order | the most time will be the restaurant but sometimes could be from our side
    added_by = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    # the driver will deliver the order
    driver = models.ForeignKey(Driver, null=True, on_delete=models.CASCADE)
    # where the driver should deliver the order | the customer's address
    # we put the address in order table because the customer could order for someone else with different address
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)


class OrderItem(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)  # id
    name = models.CharField(max_length=255)  # the order name that has been added by the agent
    description = models.TextField()  # the description for the added order
    # the order code | at lease 6 digits (we can use regEXP to specify that or random number consists of 6 digits)
    code = models.IntegerField()


# we add this table to prevent redundancy in order item table because the same order could choose more than one time
class OrderData(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, verbose_name='ID', default=create_guid)
    # the order item id | this item added to specific order
    order_item = models.ForeignKey(OrderItem, null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)  # the order id

