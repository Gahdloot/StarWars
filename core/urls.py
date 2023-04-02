from django.urls import path
from .views import FilmList, FilmComment
urlpatterns = [
    path('film-list/', FilmList.as_view()),
    path('comment/<int:id>', FilmComment.as_view())
    ]