from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .utils import send_verification_email, send_reset_password_email

User = get_user_model()

class SignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send verification email
            try:
                send_verification_email(user)
            except Exception as e:
                # Log error but still create user
                print(f"Failed to send verification email: {e}")
            
            return Response({
                'status': 'success',
                'message': 'User created successfully. Please check your email for verification.',
                'data': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                })
            return Response({
                'status': 'error',
                'message': 'Invalid email or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        
        if not token:
            return Response({
                'status': 'error',
                'message': 'Token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(verification_token=token)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Invalid or expired token'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_email_verified:
            return Response({
                'status': 'success',
                'message': 'Email already verified'
            })
        
        user.is_email_verified = True
        user.verification_token = None
        user.save()
        
        return Response({
            'status': 'success',
            'message': 'Email verified successfully'
        })
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({
                'status': 'error',
                'message': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists (security)
            return Response({
                'status': 'success',
                'message': 'If this email exists, we sent a reset link'
            })
        
        send_reset_password_email(user)
        
        return Response({
            'status': 'success',
            'message': 'If this email exists, we sent a reset link'
        })

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not token or not new_password or not confirm_password:
            return Response({
                'status': 'error',
                'message': 'All fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password != confirm_password:
            return Response({
                'status': 'error',
                'message': 'Passwords do not match'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(new_password) < 8:
            return Response({
                'status': 'error',
                'message': 'Password must be at least 8 characters'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(reset_token=token)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Invalid or expired token'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if token expired (1 hour)
        if user.last_login:
            time_diff = timezone.now() - user.last_login
            if time_diff > timedelta(hours=1):
                return Response({
                    'status': 'error',
                    'message': 'Token has expired'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.reset_token = None
        user.save()
        
        return Response({
            'status': 'success',
            'message': 'Password reset successfully'
        })
        
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        total_users = User.objects.count()
        today = timezone.now().date()
        new_users_today = User.objects.filter(date_joined__date=today).count()
        
        # Get 5 most recent users
        recent_users = User.objects.order_by('-date_joined')[:5]
        recent_users_data = [
            {
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M')
            }
            for user in recent_users
        ]
        
        return Response({
            'total_users': total_users,
            'new_users_today': new_users_today,
            'recent_users': recent_users_data
        })

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

def api_root(request):
    return JsonResponse({
        "message": "Welcome to the API",
        "available_endpoints": {
            "signup": "/api/auth/signup/",
            "login": "/api/auth/login/",
            "verify_email": "/api/auth/verify-email/",
            "forgot_password": "/api/auth/forgot-password/",
            "reset_password": "/api/auth/reset-password/",
            "dashboard_stats": "/api/dashboard/stats/",
            "user_profile": "/api/user/profile/",
            "admin": "/admin/"
        }
    })