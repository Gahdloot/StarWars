from rest_framework import serializers
from .models import Film, Comment

class FilmSerializer(serializers.ModelSerializer):


    class Meta:
        model = Film
        fields = ('id', 'title', 'episode_id', 'release_date', 'comment_count')

class FilmCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Film
        fields = ('title', 'episode_id', 'release_date',)


class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'film', 'comment', 'created_at')