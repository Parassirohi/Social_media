from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
# router.register('users', views.)
router.register('posts', views.PostViewSet)

urlpatterns = router.urls + [path("user/", views.user_profile), 
                             path("follow/<int:id>", views.follow_user),
                             path("unfollow/<int:id>", views.unfollow_user),
                             path("like/<int:id>", views.like_post),
                             path("unlike/<int:id>", views.unlike_post),
                             path("comment/<int:id>", views.comment_post),
                             path("all_post/", views.all_post),
                             ] 

