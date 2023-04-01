from django.urls import path
from . import views

#URLConfig
urlpatterns = [
    path('hello/', views.say_hello),
    path('', views.home, name="home"),
    path('calculate/', views.calculate)
]