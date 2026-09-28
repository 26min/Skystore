from catalog.forms import ProductForm
from catalog.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView


class ProductListView(ListView):
    """Главная — доступна всем"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        """Показываем только опубликованные товары"""
        return Product.objects.filter(is_published=True)


class ProductDetailView(DetailView):
    """Детали — доступна всем"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


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
