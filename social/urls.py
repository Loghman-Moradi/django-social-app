from django.urls.conf import path

from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'social'


urlpatterns = [
    path('', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('ticket/', views.ticket, name='ticket'),
    path('user_ticket/', views.user_ticket, name='user_ticket'),
    path('change_password/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url="done"), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url="/password_reset_complete"), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('posts/', views.post_list, name='posts'),
    path('posts/post/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('posts/create_post/', views.create_post, name='create_post'),
    path('post_detail/<slug:pk>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('posts/edit_post/<post_id>/', views.edit_post, name='edit_post'),
    path('posts/delete_post/<post_id>/', views.delete_post, name='delete_post'),
    path('posts/delete_image/<image_id>/', views.delete_image, name='delete_image'),
    path('like_post/', views.like_post, name='like_post'),
    path('save-post/', views.save_post, name='save_post'),
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('follow/', views.user_follow, name='user_follow'),
    path('user/<int:user_id>/followers/', views.user_followers, name='user_followers'),
    path('user/<int:user_id>/following/', views.user_following, name='user_following'),

]