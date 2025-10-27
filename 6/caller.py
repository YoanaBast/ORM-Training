import os
import django
from decimal import Decimal

from django.db import models
from django.db.models import QuerySet, Case, When, F, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
# Create queries within functions

def create_pet(name: str, species: str):
    """
    INSERT INTO
        pets("name", "species")
    VALUES
        (name, species)
    RETURNING *;
    """
    pet = Pet(name=name, species=species)
    pet.save()

    # pet = Pet.objects.create(
    #     name=name,
    #     species=species
    # )

    # pet_data = [
    #     ("Buddy", "Dog"),
    #     ("Whiskers", "Cat"),
    #     ("Goldie", "Fish"),
    #     ("Chirpy", "Bird"),
    # ]
    #
    # # Create list of unsaved Pet instances
    # pets_to_create = [Pet(name=name, species=species) for name, species in pet_data]
    #
    # # Perform one bulk insert
    # Pet.objects.bulk_create(pets_to_create)

    return f"{name} is a very cute {species}!"

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    art = Artifact(name=name, origin=origin, age=age, description=description, is_magical=is_magical)
    art.save()
    return f"The artifact {name} is {age} years old!"

def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts():
    Artifact.objects.all().delete()

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
#
# artifact_object = Artifact.objects.get(name='Ancient Sword')
#
# rename_artifact(artifact_object, 'Ancient Shield')
#
# print(artifact_object.name)

def show_all_locations():
    """
    SELECT * FROM locations
    ORDER BY id DESC;
    """

    result = ''
    for location in Location.objects.all():
        result += f"\n{location.name} has a population of {location.population}!"

    return result

def new_capital():
    """
    Option: 1
    SELECT * FROM locations
    LIMIT 1;

    UPDATE locations
    SET is_capital = True
    WHERE id = some_id;

    ---
    """
    first_location = Location.objects.first()
    first_location.is_capital = True #AttributeError: 'NoneType' object has no attribute 'is_capital' If there are no records in that table, it returns None.
    first_location.save()

def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')

def delete_first_location():
    Location.objects.first().delete()

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        sum_year = Decimal(str(sum(int(d) for d in str(car.year)) / 100))
        car.price_with_discount = car.price - (car.price * sum_year)
        car.save()

def get_recent_cars():
    """
    SELECT model, price_with_discount FROM cars WHERE year > 2020;
    """
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')

def delete_last_car():
    Car.objects.last().delete()

# print(apply_discount())
# print(get_recent_cars())

def show_unfinished_tasks():
    # breakpoint()
    tasks = Task.objects.filter(is_finished=False).values('title', 'due_date')
    result = ''
    for task in tasks: #{'title': 'Sample Task', 'due_date': datetime.date(2023, 10, 31)}
        result += f"\nTask - {task['title']} needs to be done until {task['due_date']}!"

    return result

# print(show_unfinished_tasks())

def complete_odd_tasks():
    odd_tasks = Task.objects.filter(id__mod=(2, 1))  # id % 2 == 1
    for odd_task in odd_tasks:
        odd_task.is_finished = True
        odd_task.save()

def encode_and_replace(text: str, task_title: str):
    decoded = "".join(map(chr, [(ord(c) - 3) for c in text]))
    task = Task.objects.get(title=task_title)
    task.description = decoded
    task.save()

# encode_and_replace("Zdvk#wkh#glvkhv$", "Sample Task")
# print(Task.objects.get(title='Sample Task').description)

def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type='Deluxe')
    odd_rooms = [r for r in rooms if r.id % 2 == 0]
    result = ''
    for room in odd_rooms:
        result += f"\nDeluxe room with number {room.room_number} costs {room.price_per_night}$ per night!"
    return result

# print(get_deluxe_rooms())

def increase_room_capacity():
    rooms = HotelRoom.objects.filter(is_reserved=True)
    for room in rooms:
        try:
            previous_room = HotelRoom.objects.get(id=(room.id - 1))
        except HotelRoom.DoesNotExist:
            previous_room = None

        if not previous_room:
            room.capacity = room.capacity + room.id
        else:
            room.capacity = room.capacity + previous_room.capacity
        room.save()

# increase_room_capacity()

def reserve_first_room():
    f_room = HotelRoom.objects.first()
    f_room.is_reserved = True
    f_room.save()

def delete_last_room():
    l_room = HotelRoom.objects.last()
    if l_room and not l_room.is_reserved:
        l_room.delete()

# print(get_deluxe_rooms())
# reserve_first_room()
# print(HotelRoom.objects.get(room_number=401).is_reserved)

def update_characters() -> None:
    """
    UPDATE characters
    SET
        level = CASE
            WHEN class_name = 'Mage' THEN level + 3
            ELSE level
        END
        intelligence = CASE ... END
    """

    Character.objects.update(
        level=Case(
            When(class_name='Mage', then=F('level') + 3),
            default=F('level')
        ),
        intelligence=Case(
            When(class_name='Mage', then=F('intelligence') - 7),
            default=F('intelligence')
        ),
        hit_points=Case(
            When(class_name='Warrior', then=F('hit_points') / 2),
            default=F('hit_points')
        ),
        dexterity=Case(
            When(class_name='Warrior', then=F('dexterity') + 4),
            default=F('dexterity')
        ),
        inventory=Case(
            When(class_name__in=['Assassin', 'Scout'], then=Value('The inventory is empty')),
            default=F('inventory')
        )
    )

class CharacterTypeChoices(models.TextChoices):
    MAGE = "Mage", "Mage"
    WARRIOR = "Warrior", "Warrior"
    ASSASSIN = "Assassin", "Assassin"
    SCOUT = "Scout", "Scout"
    FUSION = "Fusion", "Fusion"

def fuse_characters(first_character: Character, second_character: Character) -> None:
    inventory = None

    if first_character.class_name in [CharacterTypeChoices.MAGE, CharacterTypeChoices.SCOUT]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [CharacterTypeChoices.WARRIOR, CharacterTypeChoices.ASSASSIN]:
        inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=CharacterTypeChoices.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()

def grand_dexterity() -> None:
    """
    UPDATE main_app_character
    SET dexterity = 30;
    """
    Character.objects.update(dexterity=30)

def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)

def grand_strength() -> None:
    Character.objects.update(strength=50)

def delete_characters() -> None:
    """
    DELETE FROM main_app_character WHERE inventory = 'The inventory is empty';
    """
    Character.objects.filter(inventory='The inventory is empty').delete()