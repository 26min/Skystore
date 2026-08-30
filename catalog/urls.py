from catalog import views
from django.urls import path

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home_alt"),
    path("contacts/", views.contacts, name="contacts"),  # <-- contacts должна быть!
]

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),
    path('contacts/', views.contacts, name='contacts'),

    # НОВЫЙ МАРШРУТ ДЛЯ СТРАНИЦЫ ТОВАРА
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
]
