from django.urls import path
# from . import views
from .views import HomeView, Post_Details_View, Post_Add_View, Post_Update_View, Post_Delete_View, Post_List_View
from .views import Likes_View, Profile_View, Profile_Edit_View, Comment_Add_View, Follows_View, Comment_Delete_View, Profile_List_View, Profile_Search_View


urlpatterns = [
    # path('', views.home, name="home"),
    path('', HomeView.as_view(), name="home"),
    path('post_list/', Post_List_View.as_view(), name="post_list"),
    path('post/<int:pk>', Post_Details_View.as_view(), name="post_details"),
    path('post_add/', Post_Add_View.as_view(), name="post_add"),
    path('post/update/<int:pk>', Post_Update_View.as_view(), name="post_update"),
    path('post/<int:pk>/delete', Post_Delete_View.as_view(), name="post_delete"),
    path('likes/<int:pk>', Likes_View, name="post_like"),
    path('follows/<int:pk>', Follows_View, name="profile_followers"),
    # path('<int:pk>/profile', Profile_View.as_view(), name="profile_details"),
    path('profile/<int:pk>', Profile_View.as_view(), name="profile_details"),
    path('<int:pk>/profile_edit', Profile_Edit_View.as_view(), name="profile_edit"),
    path('post/<int:pk>/comment', Comment_Add_View.as_view(), name="comment_add"),
    path('comment/<int:pk>/delete', Comment_Delete_View.as_view(), name="comment_delete"),

    path('users_list/', Profile_List_View.as_view(), name="users_list"),
    path('search_users/', Profile_Search_View.as_view(), name="search_users"),

]