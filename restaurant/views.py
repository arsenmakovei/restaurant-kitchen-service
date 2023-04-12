from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from restaurant.forms import DishTypeSearchForm, DishSearchForm, CookSearchForm
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


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "restaurant/dish_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = DishTypeSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = DishTypeSearchForm(self.request.GET)

        if form.is_valid():
            return DishType.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    context_object_name = "dish_type"
    template_name = "restaurant/dish_type_detail.html"


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = DishSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")

        form = DishSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = CookSearchForm(initial={"username": username})

        return context

    def get_queryset(self):
        form = CookSearchForm(self.request.GET)

        if form.is_valid():
            return Cook.objects.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return self.queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
