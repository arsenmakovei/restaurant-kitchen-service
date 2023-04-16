from django.contrib.auth import get_user_model
from django.test import TestCase

from restaurant.models import DishType, Dish


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.dish_type = DishType.objects.create(
            name="Soups"
        )
        self.dish = Dish.objects.create(
            name="Tomato Soup",
            price=100,
            dish_type=self.dish_type)
        self.cook = get_user_model().objects.create_user(
            username="admin",
            password="admin12345",
            first_name="Keanu",
            last_name="Reeves"
        )

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_cook_str(self):
        self.assertEqual(
            str(self.cook),
            f"{self.cook.username} "
            f"({self.cook.first_name} {self.cook.last_name})"
        )

    def test_dish_str(self):
        self.assertEqual(str(self.dish), self.dish.name)

    def test_create_cook_with_years_of_experience(self):
        username = "admin2"
        password = "admin12345"
        years_of_experience = 10
        self.cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEqual(self.cook.username, username)
        self.assertTrue(self.cook.check_password(password))
        self.assertEqual(self.cook.years_of_experience, years_of_experience)

    def test_dish_type_get_absolute_url(self):
        expected_url = f"/dish-types/{self.dish_type.pk}/"

        self.assertEqual(self.dish_type.get_absolute_url(), expected_url)

    def test_dish_get_absolute_url(self):
        expected_url = f"/dishes/{self.dish.pk}/"

        self.assertEqual(self.dish.get_absolute_url(), expected_url)

    def test_cook_get_absolute_url(self):
        expected_url = f"/cooks/{self.cook.pk}/"

        self.assertEqual(self.cook.get_absolute_url(), expected_url)
