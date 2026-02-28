from django.urls import path
from .views import (
    CreateReferralPostView,
    ReferralPostListView,
    post_list_page
)

from .views import create_post_page


urlpatterns = [
    # API routes
    path('create-post/', CreateReferralPostView.as_view()),
    path('posts/', ReferralPostListView.as_view()),

    # UI routes
    path('posts-page/', post_list_page, name='posts_page'),
    path('posts-page/', post_list_page, name='posts_page'),
    path('create-post-page/', create_post_page, name='create_post_page'),
]