from django.urls import path
from .views import user_login, user_register, user_logout
from django.contrib.auth.views import (
    # LoginView,
    # LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    
    )

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('singup/', user_register, name='user_register'),
]