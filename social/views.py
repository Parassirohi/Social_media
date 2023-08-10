import json
from django.db.models import Count

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from .models import Post, Like, Comment, Follow
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, FollowSerializer, CommentDescriptionSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class = PostSerializer
    
    
    def list(self, request, *args, **kwargs):
        user = request.user
        user_posts = Post.objects.filter(user_id=user.pk)
        serializer = self.get_serializer(user_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, *args, **kwargs):
        
        
        user_post = self.get_object()
        
        if(user_post.user.id != request.user.id):
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

            
        likes_count = Like.objects.filter(post_id=user_post.id).count()
        comment_count = Comment.objects.filter(post_id=user_post.id).count()
        serializer = self.get_serializer(user_post)
        data = {
            "post":serializer.data,
            "likes":likes_count,
            "comments":comment_count
            }
        return Response(data, status=status.HTTP_200_OK)
    
    
    def create(self, request, *args, **kwargs):
        
        postData = request.data
        print(request.data)

        if("title" not in postData or "description" not in postData):
            return Response({"message": "Invalid data in post"}, status=status.HTTP_400_BAD_REQUEST)
        
        post = self.get_serializer(data={'title': postData.get("title"), 'user': request.user.id, 'description':postData.get("description")})
        if not post.is_valid():
            print(post.errors)
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        
        post.save()
        return Response(post.data, status=status.HTTP_200_OK)
         
        

            
        
        
        
        

    
    
class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    User = get_user_model()
    try:
        user_profile = User.objects.get(pk=user.pk)
        followers_count = Follow.objects.filter(follower=user_profile).count()
        following_count = Follow.objects.filter(following=user_profile).count()
        data = {
            "user_name": user_profile.username,
            "count_followers" : followers_count,
            "count_following": following_count 
        }
        return Response(data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])  
@permission_classes([IsAuthenticated])    
def follow_user(request,id):
    User = get_user_model() 
    user_to_follow = get_object_or_404(User, id=id)
    if user_to_follow == request.user:
        return Response({"detail": "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
    
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])  
@permission_classes([IsAuthenticated])  
def unfollow_user(request,id):
    User = get_user_model() 
    user_to_unfollow = get_object_or_404(User, id=id)
    try:
        follow_obj = Follow.objects.get(follower=request.user, following=user_to_unfollow)
        follow_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Follow.DoesNotExist:
        return Response({"detail": "You were not following this user"}, status=status.HTTP_400_BAD_REQUEST)

@api_view([])
@permission_classes([IsAuthenticated])  
def like_post(request,id):
    post = get_object_or_404(Post, id=id)
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response({"detail": "You've already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
    
    Like.objects.create(user=request.user, post=post)
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])  
@permission_classes([IsAuthenticated])  
def unlike_post(request,id):
    post = get_object_or_404(Post, id=id)
    try:
        like_obj = Like.objects.get(user=request.user, post=post)
        like_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response({"detail": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])  
@permission_classes([IsAuthenticated])  
def comment_post(request,id):
    post = get_object_or_404(Post, id=id)
    content = request.data.get('description')
    if not content:
        return Response({"detail": "Description is required for commenting"}, status=status.HTTP_400_BAD_REQUEST)
    
    created_comment = Comment.objects.create(user=request.user, post=post, description=content)
    return Response({"comment_id": created_comment.id}  ,status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_post(request):
    user = request.user
    posts = Post.objects.filter(user_id=user.id).order_by('created_at')
    
    serialized_posts = []
    for post in posts:
        serialized_post = PostSerializer(post, context={'request': request}).data
        comments = post.comment_set.all()
        serialized_comments = CommentDescriptionSerializer(comments, many=True).data
        serialized_post['comments'] = serialized_comments
        serialized_post['like_count'] = post.like_set.count()
        serialized_posts.append(serialized_post)
    
    return Response(serialized_posts, status=status.HTTP_200_OK)

    
    
