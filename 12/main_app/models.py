from datetime import timedelta, date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet


# Create your models here.

class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True

class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)

class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)

class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)

class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)

class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)

class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)

class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)

class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)

class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)



class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self) -> None:
        self.is_read = True
        self.save()

    def reply_to_message(self, reply_content: str):
        m = Message.objects.create(sender=self.receiver, receiver=self.sender, content=reply_content)
        m.save()
        return m

    def forward_message(self, receiver: UserProfile):
        m = Message.objects.create(sender=self.receiver, receiver=receiver, content=self.content)
        m.save()
        return m


class StudentIDField(models.PositiveIntegerField):
    """
    accepts floats, strings (string numbers), negative string numbers, and negative numbers.
    """
    def to_python(self, value):
        if value is None:
            return value
        try:
            return int(float(value))
        except ValueError:
            raise ValueError("Invalid input for student ID")

    def get_prep_value(self, value):
        super().get_prep_value(value)
        if value <= 0:
            raise ValidationError("ID cannot be less than or equal to zero")
        return value

class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()



class MaskedCreditCardField(models.CharField):

    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)


    def to_python(self, value):
        if value is None:
            return None

        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if not len(value) == 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return value

    def get_prep_value(self, value):

        value = self.to_python(value)

        return "****-****-****-" + value[-4:]

class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField(max_length=20)


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")


    def save(self, *args, **kwargs):
        self.clean()  # validate first
        super().save(*args, **kwargs)  # save the instance
        return f"Room {self.number} created successfully"

class BaseReservation(models.Model):
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self) -> int:
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self) -> Decimal:
        total_cost = self.reservation_period() * self.room.price_per_night
        return round(total_cost, 2)

    def get_overlapping_reservations(self, start_date: date, end_date: date) -> QuerySet['BaseReservation']:
        return self.__class__.objects.filter(
            room=self.room,
            end_date__gte=start_date,
            start_date__lte=end_date,
            # ~Q(pk=self.pk)  where reservation is not the same
        )

    @property
    def is_available(self) -> bool:
        return not self.get_overlapping_reservations(self.start_date, self.end_date).exists()

    def clean(self) -> None:
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if not self.is_available:
            raise ValidationError("Room {room_number} cannot be reserved")

    @property
    def reservation_type(self) -> str:
        raise NotImplemented

    def save(self, *args, **kwargs) -> str:
        self.clean()
        super().save(*args, **kwargs)

        return f"{self.reservation_type} reservation for room {self.room.number}"

    class Meta:
        abstract = True


class RegularReservation(BaseReservation):
    @property
    def reservation_type(self) -> str:
        return "Regular"


class SpecialReservation(BaseReservation):
    @property
    def reservation_type(self) -> str:
        return "Special"

    def extend_reservation(self, days: int) -> str:
        new_end_date = self.end_date + timedelta(days=days)
        reservations = self.get_overlapping_reservations(self.start_date, new_end_date)

        if reservations:
            raise ValidationError("Error during extending reservation")

        self.end_date = new_end_date
        self.save()

        # Option 2
        # self.end_date += timedelta(days=days)
        #
        # if not self.is_available:
        #     self.end_date -= timedelta(days=days)
        #     raise ValidationError("Error during extending reservation")
        #
        # self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"