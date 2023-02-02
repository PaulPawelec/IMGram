from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="register"),
    path('user_edit/', views.UserEditView.as_view(), name="user_edit"),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html')),
    path('password/', views.ChangePasswordView.as_view(template_name='registration/password_change.html')),
    path('password_success', views.password_success, name="password_success"),
]