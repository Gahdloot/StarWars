from rest_framework import serializers
from .models import Film, Comment

class FilmSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = ('id', 'title', 'release_date', 'comment_count')



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'film', 'comment', 'created_at')