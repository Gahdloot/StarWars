from django.urls import path
from .views import FilmList
urlpatterns = [
    path('film-list/', FilmList.as_view())
    ]