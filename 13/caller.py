import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import Restaurant
from django.core.exceptions import ValidationError

# Valid restaurant
# valid_restaurant = Restaurant(
#     name="Delicious Bistro",
#     location="123 Main Street",
#     description="A cozy restaurant with a variety of dishes.",
#     rating=5.00,
# )
#
# try:
#     valid_restaurant.full_clean()
#     valid_restaurant.save()
#     print("Valid Restaurant saved successfully!")
# except ValidationError as e:
#     print(f"Validation Error: {e}")
#
# # Invalid restaurant
# invalid_restaurant = Restaurant(
#     name="A",
#     location="A" * 201,
#     description="A restaurant with a long name and invalid rating.",
#     rating=5.01,
# )
#
# try:
#     invalid_restaurant.full_clean()
#     invalid_restaurant.save()
#     print("Invalid Restaurant saved successfully!")
# except Exception as e:
#     print(f"Validation Error: {e}")

from main_app.models import Restaurant, Menu
from django.core.exceptions import ValidationError

# Keep the data from the previous exercise, so you can reuse it
#
# valid_menu = Menu(
#     name="Menu at The Delicious Bistro",
#     description=(
#         "** Appetizers: **\nSpinach and Artichoke Dip\n"
#         "** Main Course: **\nGrilled Salmon\n"
#         "** Desserts: **\nChocolate Fondue"
#     ),
#     restaurant=Restaurant.objects.first(),
# )
#
# try:
#     valid_menu.full_clean()
#     valid_menu.save()
#     print("Valid Menu saved successfully!")
# except ValidationError as e:
#     print(f"Validation Error: {e}")
#
# invalid_menu = Menu(
#     name="Incomplete Menu",
#     description="** Appetizers: **\nSpinach and Artichoke Dip",
#     restaurant=Restaurant.objects.first(),
# )
#
# try:
#     invalid_menu.full_clean()
#     invalid_menu.save()
#     print("Invalid Menu saved successfully!")
# except ValidationError as e:
#     print(f"Validation Error: {e}")

# from main_app.models import Restaurant, RestaurantReview
# from django.core.exceptions import ValidationError
#
# # Create restaurants
# restaurant1 = Restaurant.objects.create(
#     name="Restaurant A",
#     location="123 Main St.",
#     description="A cozy restaurant",
#     rating=4.88
# )
#
# restaurant2 = Restaurant.objects.create(
#     name="Restaurant B",
#     location="456 Elm St.",
#     description="Charming restaurant",
#     rating=3.59
# )
#
# # Create reviews
# RestaurantReview.objects.create(
#     reviewer_name="Bob",
#     restaurant=restaurant1,
#     review_content="Good experience overall.",
#     rating=4
# )
#
# RestaurantReview.objects.create(
#     reviewer_name="Aleks",
#     restaurant=restaurant1,
#     review_content="Great food and service!",
#     rating=5
# )
#
# RestaurantReview.objects.create(
#     reviewer_name="Charlie",
#     restaurant=restaurant2,
#     review_content="It was ok!",
#     rating=2
# )
#
# # Attempt duplicate review
# duplicate_review = RestaurantReview(
#     reviewer_name="Aleks",
#     restaurant=restaurant1,
#     review_content="Another great meal!",
#     rating=5
# )
#
# try:
#     duplicate_review.full_clean()
#     duplicate_review.save()
# except ValidationError as e:
#     print(f"Validation Error: {e}")
#
# # Print all reviews
# print("All Restaurant Reviews:")
# for review in RestaurantReview.objects.all():
#     print(f"Reviewer: {review.reviewer_name}, Rating: {review.rating}, Restaurant: {review.restaurant.name}")
# from main_app.models import Restaurant, RegularRestaurantReview, FoodCriticRestaurantReview
# from django.core.exceptions import ValidationError
#
# # Create restaurant
# restaurant1 = Restaurant.objects.create(
#     name="Restaurant A",
#     location="123 Main St.",
#     description="A cozy restaurant",
#     rating=4.88
# )
#
# # Create regular reviews
# RegularRestaurantReview.objects.create(
#     reviewer_name="Bob",
#     restaurant=restaurant1,
#     review_content="Good experience overall.",
#     rating=4
# )
#
# RegularRestaurantReview.objects.create(
#     reviewer_name="Aleks",
#     restaurant=restaurant1,
#     review_content="Great food and service!",
#     rating=5
# )
#
# # Attempt duplicate review
# duplicate_review = RegularRestaurantReview(
#     reviewer_name="Aleks",
#     restaurant=restaurant1,
#     review_content="Another great meal!",
#     rating=5
# )
#
# try:
#     duplicate_review.full_clean()
#     duplicate_review.save()
# except ValidationError as e:
#     print(f"Validation Error: {e}")
#
# # Print model information
# print("Regular Restaurant Review:")
# print(f"Model Name: {RegularRestaurantReview._meta.verbose_name}")
# print(f"Model Plural Name: {RegularRestaurantReview._meta.verbose_name_plural}")
#
# print("Food Critic Restaurant Review:")
# print(f"Model Name: {FoodCriticRestaurantReview._meta.verbose_name}")
# print(f"Model Plural Name: {FoodCriticRestaurantReview._meta.verbose_name_plural}")

# from main_app.models import RegularRestaurantReview, Restaurant, MenuReview, Menu
#
# # Create restaurant
# Restaurant.objects.create(
#     name="Savory Delight",
#     location="456 Elm Avenue",
#     rating=4.2,
# )
#
# restaurant_from_db = Restaurant.objects.get(name="Savory Delight")
#
# # Create regular restaurant review
# RegularRestaurantReview.objects.create(
#     reviewer_name="Alice",
#     restaurant=restaurant_from_db,
#     rating=4,
#     review_content="Good experience overall."
# )
#
# review_from_db = RegularRestaurantReview.objects.get(
#     reviewer_name="Alice",
#     restaurant=restaurant_from_db
# )
#
# print(
#     f"Reviewer name: {review_from_db.reviewer_name}\n"
#     f"Restaurant: {review_from_db.restaurant.name}\n"
#     f"Rating: {review_from_db.rating}\n"
#     f"Review content: {review_from_db.review_content}"
# )
#
# # Create menu
# Menu.objects.create(
#     name="Delightful Food Menu",
#     description=(
#         "Appetizers:\nSpinach and Artichoke Dip\n"
#         "Main Course:\nGrilled Salmon\n"
#         "Desserts:\nChocolate Fondue"
#     ),
#     restaurant=restaurant_from_db
# )
#
# menu_from_db = Menu.objects.get(name="Delightful Food Menu")
#
# # Create menu review
# MenuReview.objects.create(
#     reviewer_name="Lilly",
#     menu=menu_from_db,
#     rating=5,
#     review_content="Delicious food"
# )
#
# menu_review_from_db = MenuReview.objects.get(
#     reviewer_name="Lilly",
#     menu=menu_from_db
# )
#
# print(
#     f"Reviewer name: {menu_review_from_db.reviewer_name}\n"
#     f"Menu: {menu_review_from_db.menu.name}\n"
#     f"Rating: {menu_review_from_db.rating}\n"
#     f"Review content: {menu_review_from_db.review_content}"
# )
