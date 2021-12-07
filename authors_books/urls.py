from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="author_list"),
    path('titles/<str:pk>/', views.book_list, name="titles_list")
]