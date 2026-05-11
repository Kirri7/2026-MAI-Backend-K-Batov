from django.urls import path
from . import views

# -> localhost:8000/dbapp/.../

urlpatterns = [
    path('search', views.search_courses),
    path('courses/', views.list_courses),
    path('courses/create', views.create_course),
]
