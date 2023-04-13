from django.contrib.auth import get_user_model
from django.test import TestCase

from restaurant.models import DishType, Dish, Cook
from restaurant.forms import DishTypeSearchForm, DishSearchForm, CookSearchForm


class SearchFormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test", password="test1234"
        )
        self.client.force_login(self.user)

        self.dish_type1 = DishType.objects.create(name="Soups")
        self.dish_type2 = DishType.objects.create(name="Salads")

    def test_dish_type_get_context_data_with_search_form(self):
        url = "/dish-types/"
        data = {"name": "So"}

        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            DishTypeSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "So"
        )

    def test_dish_get_context_data_with_search_form(self):
        self.dish1 = Dish.objects.create(
            name="Cezar Salad",
            price=100,
            dish_type=self.dish_type1,
        )
        self.dish2 = Dish.objects.create(
            name="Greek Salad",
            price=150,
            dish_type=self.dish_type2,
        )

        url = "/dishes/"
        data = {"name": "salad"}

        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            DishSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "salad"
        )

    def test_cook_get_context_data_with_search_form(self):
        self.cook1 = get_user_model().objects.create_user(
            username="admin101", password="admin3476",
        )
        self.cook2 = get_user_model().objects.create_user(
            username="best.cook", password="super.cook",
        )

        url = "/cooks/"
        data = {"username": "admin"}

        response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            CookSearchForm
        )
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "admin"
        )
