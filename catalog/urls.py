from catalog import views
from django.urls import path

app_name = "catalog"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("home/", views.ProductListView.as_view(), name="home_alt"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update/", views.ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
]
