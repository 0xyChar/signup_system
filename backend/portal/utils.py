import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def send_verification_email(user):
    """Send email verification link to user"""
    token = generate_token()
    user.verification_token = token
    user.save()
    
    verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    subject = 'Verify Your Email'
    message = f"""
    Hi {user.username},
    
    Please click the link below to verify your email address:
    {verification_link}
    
    This link expires in 24 hours.
    
    If you didn't sign up for this account, please ignore this email.
    
    Best,
    Charity
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_reset_password_email(user):
    """Send password reset link to user"""
    token = generate_token()
    user.reset_token = token
    user.save()
    
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    subject = 'Reset Your Password'
    message = f"""
    Hello there {user.username},
    
    I have  received a request to reset your password.
    Click the link below to reset it:
    {reset_link}
    
    This link expires in 1 hour.
    
    If you did not  request this, please ignore this email.
    
    Best,
    Charity
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )