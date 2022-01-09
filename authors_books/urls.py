from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name="author_list"),
    path('titles/<str:pk>/', views.book_list, name="titles_list"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
]