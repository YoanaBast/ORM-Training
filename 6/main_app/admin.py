from django.contrib import admin
from django.db import models
from .models import Pet, Artifact, Location, Car, Task, HotelRoom, Character

# Register your models here.
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "species")

@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ("name", "origin", 'age', 'description', 'is_magical')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "region", 'population', 'description', 'is_capital')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("model", "year", 'price', 'price_with_discount')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "due_date", 'is_finished')

@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "price_per_night", "is_reserved", "capacity")

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "class_name",
        "level",
        "strength",
        "dexterity",
        "intelligence",
        "hit_points",
        "inventory",
    )