from django.contrib import admin

# Register your models here.
from .models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Car, Registration, Owner


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["model", "year", "owner", "car_details"]

    @staticmethod
    def car_details(obj: Car):
        try:
            owner_name = obj.owner.name
        except AttributeError:
            owner_name = "No owner"

        try:
            plate = obj.registration.registration_number
        except AttributeError:
            plate = "No registration number"

        return f"Owner: {owner_name}, Registration: {plate}"

    car_details.short_description = "Car Details"