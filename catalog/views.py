from catalog.forms import ProductForm
from catalog.models import Category, Product
from catalog.services import get_all_products, get_products_by_category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView


class ProductListView(ListView):
    """Главная — доступна всем, кэшируется через сервис"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = get_all_products()
        return context


# class ProductDetailView(DetailView):
#     """Детали — доступна всем"""
#
#     model = Product
#     template_name = "catalog/product_detail.html"
#     context_object_name = "product"


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание — только авторизованным"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")
    login_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Привязываем продукт к текущему пользователю"""
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование — только владелец"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")
    login_url = reverse_lazy("users:login")

    def test_func(self):
        """Проверяем, что пользователь — владелец продукта"""
        product = self.get_object()
        return product.owner == self.request.user


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление — только владелец или модератор"""

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
    login_url = reverse_lazy("users:login")

    def test_func(self):
        """Проверяем, что пользователь — владелец ИЛИ модератор"""
        product = self.get_object()
        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.has_perm("catalog.delete_product")
        return is_owner or is_moderator


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(DetailView):
    """Детали товара — кэшируется на 15 минут"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class CategoryProductsView(DetailView):
    """Страница со списком продуктов в категории"""

    model = Category
    template_name = "catalog/category_products.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        """Добавляем список продуктов из сервиса"""
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("pk")
        context["products"] = get_products_by_category(category_id)
        return context
