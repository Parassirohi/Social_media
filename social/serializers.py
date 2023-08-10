from rest_framework import serializers
from .models import Post, Like, Follow,  Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        
class CommentDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['description', 'user']
        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

