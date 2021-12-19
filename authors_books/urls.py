from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="author_list"),
    path('titles/<str:pk>/', views.book_list, name="titles_list"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]