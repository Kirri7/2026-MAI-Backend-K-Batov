from django.urls import path
from . import views

# -> localhost:8000/myapi/profile/

urlpatterns = [
    path('profile/', views.get_profile),
    path('products/', views.get_products),
    path('category/<int:category_id>/', views.get_category),
]