from django.urls import path
from . import views

urlpatterns = [
    path('', views.anime_search, name="search_bar"),
    path('details/<int:question_id>/', views.detail, name = "details")
]