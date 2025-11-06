from datetime import date
from random import choices

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import TextChoices


# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        today = date.today()
        years = today.year - self.birth_date.year
        # subtract 1 if birthday hasn’t occurred yet this year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

class Mammal(Animal):
    fur_color = models.CharField(max_length=50)


class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5, decimal_places=2)

class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)

    class Meta:
        abstract = True  # prevents Django from creating a table for this model

class ZooKeeper(Employee):
    class SpecChoices(models.TextChoices):
        Mammals = "Mammals", "Mammals"
        Birds = "Birds", "Birds"
        Reptiles = "Reptiles", "Reptiles"
        Others = "Others", "Others"
    specialty = models.CharField(max_length=10, choices=SpecChoices.choices)
    managed_animals = models.ManyToManyField(Animal)

    def clean(self):
        if self.specialty not in self.SpecChoices.values:
            raise ValidationError("Specialty must be a valid choice.")

    def save(self, *args, **kwargs):
        self.full_clean()  # triggers the clean() method
        super().save(*args, **kwargs)

class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        # Set choices and default
        kwargs['choices'] = ((True, "Available"), (False, "Not Available"))
        kwargs.setdefault('default', True)
        super().__init__(*args, **kwargs)

class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()

class ZooDisplayAnimal(Animal):
    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."

    def is_endangered(self):
        if self.species in ["Cross River Gorilla", "Orangutan", "Green Turtle"]:
            return f"{self.species} is at risk!"
        return f"{self.species} is not at risk."

    class Meta:
        proxy = True


