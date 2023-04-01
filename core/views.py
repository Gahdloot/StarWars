from django.shortcuts import render
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Film, Comment
from .serializer import FilmSerializer, CommentSerializer, FilmCreationSerializer
from .film_api import Swapi
import requests
import json
from datetime import datetime
# Create your views here.


class FilmList(APIView):

    def get(self, request):
        cache_key = 'films_list'
        films = cache.get(cache_key)
        if not films:
            try:
                if Film.objects.all().count() < 6:
                    response = requests.get('https://swapi.dev/api/films/')
                    if response.status_code != 200:
                        return Response({'Success': False, 'message': 'Films not found'}, status=status.HTTP_404_NOT_FOUND)
                    data = Swapi().get_list(response)
                    for data in data:
                        if Film.objects.get(episode_id=data['episode_id']).exist() is False:
                            serializer = FilmCreationSerializer(data=data)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()

                query = Film.objects.all()
                query = FilmSerializer(query, many=True)
                film_list = query.data
                films = film_list
                cache.set(cache_key, films, 60 * 60 * 24 )
                return Response({'Success': True, 'data': films, 'message': 'data is gotten from database'}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'Success': False, 'message': e}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Success': True, 'data': films, 'message': 'data is gotten from cache'}, status=status.HTTP_200_OK)



