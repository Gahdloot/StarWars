from django.shortcuts import render
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Film, Comment
from .serializer import FilmSerializer, GetCommentSerializer, FilmCreationSerializer
from .film_api import Swapi
import requests
import json
from datetime import datetime
# Create your views here.


class FilmList(APIView):

    def get(self, request):
        cache_key = 'films_list'
        films = cache.get(cache_key)
        """Check if data is cached"""
        if not films:
            try:
                """Check if database already contains api data"""
                if Film.objects.all().count() < 6:
                    response = requests.get('https://swapi.dev/api/films/')
                    if response.status_code != 200:
                        return Response({'Success': False, 'message': 'Films not found'}, status=status.HTTP_404_NOT_FOUND)
                    data = Swapi().get_list(response)
                    """Add all Data to database"""
                    for data in data:
                        if Film.objects.get(episode_id=data['episode_id']).exist() is False:
                            serializer = FilmCreationSerializer(data=data)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                """if database already contains data, but not in cache, get queryset """
                query = Film.objects.all()
                query = FilmSerializer(query, many=True)
                film_list = query.data
                films = film_list
                """Set Cache"""
                cache.set(cache_key, films, 60 * 60 * 24 )
                return Response({'Success': True, 'data': films, 'message': 'data is gotten from database'}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'Success': False, 'message': e}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Success': True, 'data': films, 'message': 'data is gotten from cache'}, status=status.HTTP_200_OK)


class FilmComment(APIView):
    def post(self, request, id):
        """Check that comment is not empty or contains less than 500 characters"""
        if request.data['comment'] and len(request.data['comment']) <= 500:
            try:
                film = Film.objects.get(id=id)
                comment = Comment(film=film, comment=request.data['comment'])
                comment.save()
                query = Film.objects.all()
                query = FilmSerializer(query, many=True)
                film_list = query.data
                films = film_list
                cache_key = 'films_list'
                """Set Cache"""
                cache.set(cache_key, films, 60 * 60 * 24)
                return Response({'Success': True, 'message': 'comment created'}, status=status.HTTP_201_CREATED)
            except ObjectDoesNotExist:
                return Response({'Success': False, 'message': 'Film does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Success': False, 'message': 'Comment length is invalid'}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request, id):
        try:
            film = Film.objects.get(id=id)
            comments = Comment.objects.filter(film__id=film.id)
            serializer = GetCommentSerializer(comments, many=True)
            comment_list = serializer.data
            return Response({'Success': True, 'data': comment_list}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({'Success': False, 'message': 'Film does not exist'}, status=status.HTTP_404_NOT_FOUND)



