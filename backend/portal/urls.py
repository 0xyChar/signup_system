from django.urls import path
from . import views

urlpatterns = [
     path('', views.api_root, name='api-root'),
    path('auth/signup/', views.SignupView.as_view(), name='signup'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('auth/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard_stats'),
    path('user/profile/', views.UserProfileView.as_view(), name='user_profile'),
]