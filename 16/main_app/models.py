from decimal import Decimal

from django.db import models
from django.db.models import Q, Count, Avg
from .validators import RangeValidator

# Create your models here.
class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type: str):
        #returns all real estate objects (in a queryset) from the given property type.
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(price__range=(min_price, max_price))

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms=bedrooms_count)
        #all real estate objects (in a queryset) with the given bedroom count.

    def popular_locations(self):
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]
        #returns the 2 most visited locations, ordered by location alphabetically (ascending).
        # The most visited locations are those with the most database records.

class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    objects = RealEstateListingManager()

class VideoGameManager(models.Manager):
    def games_by_genre(self, genre: str):
        #- returns all game objects (in a queryset) from the given genr
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        #- returns all game objects (in a queryset) that are released after or in the same year as the given year.
        return self.filter(Q(release_year__gte=year))

    def highest_rated_game(self):
        #- returns the highest-rated game.
        return self.order_by('-rating').first()

    def lowest_rated_game(self):
        return self.order_by('rating').first()

    def average_rating(self):
        #- returns the calculation of the average rating of all games in the database,
        # formatted to the first decimal place, ordered by the average rating (descending).
        avg = self.aggregate(avg=Avg('rating'))['avg']
        return f"{avg:.1f}"


class VideoGame(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_year = models.PositiveIntegerField(validators=[RangeValidator(min_value=Decimal('1990'), max_value=Decimal('2023'), message="The release year must be between 1990 and 2023")])
    rating = models.DecimalField(max_digits=2,decimal_places=1, validators=[RangeValidator(min_value=Decimal('0.0'), max_value=Decimal('10.0'), message="The rating must be between 0.0 and 10.0")])

    def __str__(self):
        return self.title

    objects = VideoGameManager()

class BillingInfo(models.Model):
    address = models.CharField(max_length=200)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    billing_info = models.OneToOneField(BillingInfo, on_delete=models.CASCADE)

    @classmethod
    def get_invoices_with_prefix(cls, prefix: str):
        #- returns all the invoices (in a queryset), starting with the specific prefix in the invoice number.
        return cls.objects.filter(invoice_number__startswith=prefix)

    @classmethod
    def get_invoices_sorted_by_number(cls):
        #- returns all the invoices (in a queryset), ordered by invoice number (ascending)
        return cls.objects.all().order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number: str):
        #- returns the invoice object by a specific invoice number.
        return cls.objects.select_related('billing_info').filter(invoice_number=invoice_number).first()

class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology, related_name='projects')

    def get_programmers_with_technologies(self):
        #- returns all programmers and all technologies, related to the project (in a queryset).
        return self.programmers.prefetch_related('projects__technologies_used',)



class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, related_name='programmers')

    def get_projects_with_technologies(self):
        #- returns all projects and all technologies (for the current project), related to the programmer (in a queryset).
        return self.projects.prefetch_related('technologies_used')

class Task(models.Model):
    PRIORITIES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITIES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField()


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()
