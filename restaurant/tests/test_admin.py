from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234",
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="spiderman",
            password="spider1234",
            years_of_experience=10
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:restaurant_cook_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_driver_detailed_license_number_listed(self):
        url = reverse("admin:restaurant_cook_change", args=[self.cook.pk])
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_driver_create_license_number_listed(self):
        url = reverse("admin:restaurant_cook_add")
        response = self.client.get(url)

        self.assertContains(response, "Years of experience")
