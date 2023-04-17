from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from restaurant.forms import (
    DishTypeSearchForm,
    DishTypeForm,
    DishSearchForm,
    DishForm,
    CookSearchForm,
    CookCreationForm,
)
from restaurant.models import Cook, DishType, Dish


@login_required
def index(request):
    num_cooks = Cook.objects.count()
    num_dish_types = DishType.objects.count()
    num_dishes = Dish.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
        "num_visits": num_visits + 1,
    }

    return render(request, "restaurant/index.html", context=context)


class SearchFormMixin(generic.ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = self.search_form(initial={"name": name})

        return context


class DishTypeListView(SearchFormMixin, LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "restaurant/dish_type_list.html"
    paginate_by = 8
    search_form = DishTypeSearchForm

    def get_queryset(self):
        form = self.search_form(self.request.GET)

        if form.is_valid():
            return DishType.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    context_object_name = "dish_type"
    template_name = "restaurant/dish_type_detail.html"


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    template_name = "restaurant/dish_type_form.html"
    form_class = DishTypeForm


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    template_name = "restaurant/dish_type_form.html"
    form_class = DishTypeForm


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("restaurant:dish-type-list")
    template_name = "restaurant/dish_type_confirm_delete.html"


class DishListView(SearchFormMixin, LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 8
    search_form = DishSearchForm

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")

        form = self.search_form(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("restaurant:dish-list")


class CookListView(SearchFormMixin, LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 8
    search_form = CookSearchForm

    def get_queryset(self):
        form = self.search_form(self.request.GET)

        if form.is_valid():
            return Cook.objects.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return self.queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CookCreateView(generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "registration/register.html"


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("login")


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "years_of_experience"
    )


class ToggleAssignToDishView(LoginRequiredMixin, generic.View):
    def get(self, request, pk):
        return HttpResponseRedirect(reverse_lazy(
            "restaurant:dish-detail", args=[pk])
        )

    def post(self, request, pk):
        dish = get_object_or_404(Dish, id=pk)
        user = request.user
        if user in dish.cooks.all():
            dish.cooks.remove(user)
        else:
            dish.cooks.add(user)
        return HttpResponseRedirect(reverse_lazy(
            "restaurant:dish-detail", args=[pk])
        )
