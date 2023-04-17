from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from restaurant.forms import DishTypeSearchForm
from restaurant.models import DishType


class DishTypeListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

        self.dish_type1 = DishType.objects.create(name="Soups")
        self.dish_type2 = DishType.objects.create(name="Salads")

    def test_get_context_data(self):
        url = reverse("restaurant:dish-type-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"],
            DishTypeSearchForm
        )

    def test_get_queryset_filtered(self):
        url = reverse("restaurant:dish-type-list") + "?name=Sou"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["dish_type_list"],
            [self.dish_type1]
        )

    def test_get_queryset_not_filtered(self):
        url = reverse("restaurant:dish-type-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["dish_type_list"],
            [self.dish_type1, self.dish_type2],
            ordered=False
        )
