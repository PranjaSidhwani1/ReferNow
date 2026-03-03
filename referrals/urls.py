from django.urls import path
from .views import (
    CreateReferralPostView,
    ReferralPostListView,
    post_list_page
)

from .views import create_post_page, apply_referral, my_applications_dashboard, my_posts_dashboard,post_applicants, profile_detail, update_application_status, candidate_detail, open_chat,candidate_chat,toggle_chat


urlpatterns = [
    # API routes
    path('create-post/', CreateReferralPostView.as_view()),
    path('posts/', ReferralPostListView.as_view()),

    # UI routes
    path('posts-page/', post_list_page, name='posts_page'),
    path('posts-page/', post_list_page, name='posts_page'),
    path('create-post-page/', create_post_page, name='create_post_page'),
    path("apply/<int:referral_id>/", apply_referral, name="apply_referral"),
    path("my-applications/", my_applications_dashboard, name="my_applications"),
    path("my-posts/", my_posts_dashboard, name="my_posts"),
    path("post/<int:post_id>/applicants/", post_applicants, name="post_applicants"),
    path("profile/<int:user_id>/",profile_detail, name="profile_detail"),
    path("application/<int:app_id>/<str:action>/", update_application_status, name="update_application_status"),
    path("candidate/<int:app_id>/",candidate_detail, name="candidate_detail"),
    path("open-chat/<int:app_id>/",open_chat,name="open_chat"),
    path("chat/<int:app_id>/",candidate_chat,name="candidate_chat"),
    path("application/<int:app_id>/toggle-chat/", toggle_chat,name="toggle_chat"),

]