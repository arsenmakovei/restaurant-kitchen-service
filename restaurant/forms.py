import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from restaurant.models import Dish, Cook, DishType


def validate_first_letter_uppercase(value):
    if not value[0].isupper():
        raise ValidationError(
            "Ensure that the first letter of this value is uppercase."
        )


def validate_letters_only(value):
    pattern = r"^[a-zA-Z\s]+$"
    if not re.match(pattern, value):
        raise ValidationError("The value must contain only letters.")


class DishTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"})
    )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"})
    )


class DishForm(forms.ModelForm):
    name = forms.CharField(
        min_length=3,
        validators=[
            validate_first_letter_uppercase,
            validate_letters_only
        ],
        widget=forms.TextInput(attrs={"placeholder": "Enter dish name"}),
    )
    description = forms.CharField(
        min_length=3,
        validators=[validate_first_letter_uppercase],
        widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "Write a short description for the dish"
        }),
    )
    price = forms.DecimalField(
        min_value=0.01,
        max_value=9999.99,
        help_text="Enter a price from 0.01 to 9999.99"
    )
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Dish
        fields = "__all__"


class DishTypeForm(forms.ModelForm):
    name = forms.CharField(
        min_length=3,
        validators=[
            validate_first_letter_uppercase,
            validate_letters_only
        ],
        widget=forms.TextInput(attrs={"placeholder": "Enter dish type here"}),
    )

    class Meta:
        model = DishType
        fields = "__all__"


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "years_of_experience"
        )
