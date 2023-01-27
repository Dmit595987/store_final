from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView, UserLoginView, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login_user'),
    path('register/', UserRegistrationView.as_view(), name='register_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile_user'),
    path('verification/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
