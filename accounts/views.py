from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, logout, authenticate
from .forms import HostRegistrationForm, ResetPasswordForm, ForgotPasswordForm, UserLoginForm, UserCreationForm, UserProfileForm, UserRegistrationForm, OTPVerificationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .models import Profile, User
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
import random
from datetime import timedelta
#---------- Authentication Views ----------#

def register_host(request):
    if request.method == "POST":
        form = HostRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.role = 'host'
            user.is_active = False  # Prevent login until email verification
            user.otp_code = str(random.randint(100000, 999999))  # Generate OTP
            user.save()

            # Send OTP Email
            send_mail(
                'OTP Verification for Host Registration',
                f'Your OTP Code is {user.otp_code}. Use this to verify your email.',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )

            request.session['email'] = user.email  # Store email for OTP verification
            return redirect('accounts:verify_host_otp')  # Redirect to OTP verification page

    else:
        form = HostRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
    

def verify_host_otp(request):
    email = request.session.get('email')
    if not email:
        return redirect('accounts:register_host')

    user = get_object_or_404(User, email=email)

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if user.otp_code == otp:
                user.is_active = True
                user.otp_code = None  # Clear OTP after verification
                user.save()
                login(request, user)  # Automatically log in the user
                messages.success(request, 'Account verified and logged in successfully!')
                
                try:
                    profile = user.profile
                    if not profile.is_profile_complete:
                        return redirect('accounts:complete_profile')
                except Profile.DoesNotExist:
                    # If profile doesn't exist, create one and redirect to complete it
                    Profile.objects.create(user=user)
                    return redirect('accounts:complete_profile')

                # Redirect based on user role
                if user.role == 'host':
                    return redirect('accounts:host_dashboard')
                elif user.role == 'guest':
                    return redirect('accounts:user_dashboard')
                else:
                    return redirect('accounts:home')
            else:
                messages.error(request, 'Invalid OTP. Try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/verify_host_otp.html', {'form': form})


def verify_otp(request):
    email = request.session.get('email')
    if not email:
        return redirect('accounts:register')

    user = User.objects.get(email=email)

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if user.otp_code == otp:
                user.is_active = True
                user.otp_code = None  # Clear OTP after verification
                user.save()
                login(request, user)  # Automatically log in the user
                messages.success(request, 'Account verified and logged in successfully!')
                
                try:
                    profile = user.profile
                    if not profile.is_profile_complete:
                        return redirect('accounts:complete_profile')
                except Profile.DoesNotExist:
                    # If profile doesn't exist, create one and redirect to complete it
                    Profile.objects.create(user=user)
                    return redirect('accounts:complete_profile')

                # Redirect based on user role
                if user.role == 'host':
                    return redirect('crowdfunding:host_dashboard')
                elif user.role == 'guest':
                    return redirect('crowdfunding:user_dashboard')
                else:
                    return redirect('crowdfunding:home')

            else:
                messages.error(request, 'Invalid OTP. Try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/verify_otp.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until OTP verification
            user.otp_code = str(random.randint(100000, 999999))  # Generate OTP
            user.save()

            # Send OTP Email
            send_mail(
                'OTP Verification',
                f'Your OTP Code is {user.otp_code}',
                'noreply@example.com',
                [user.email],
                fail_silently=False,
            )
            request.session['email'] = user.email  # Store email in session for OTP verification
            return redirect('accounts:verify_otp')  # Add namespace here

    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def complete_profile(request):
    user = request.user
    now = timezone.now()
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile.is_profile_complete = True
            profile.save()
            messages.success(request, "Profile updated successfully!")
            if user.role == 'host':
                return redirect('crowdfunding:host_dashboard')
            elif user.role == 'guest':
                return redirect('crowdfunding:user_dashboard')
            else:
                return redirect('crowdfunding:home')
            
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/complete_profile.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')

                # Check if profile exists and is complete
                try:
                    profile = user.profile
                    if not profile.is_profile_complete:
                        return redirect('accounts:complete_profile')
                except Profile.DoesNotExist:
                    # If profile doesn't exist, create one and redirect to complete it
                    Profile.objects.create(user=user)
                    return redirect('accounts:complete_profile')

                # Redirect based on user role
                if user.role == 'guest':
                    return redirect('core:dashboard')
                else:
                    return redirect('core:home')

            else:
                messages.error(request, 'Invalid email or password.')

    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})



def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('accounts:login')

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    success_message = "Password reset instructions have been sent to your email."

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

##################

class ForgotPasswordView(PasswordResetView):
    template_name = 'accounts/forgot_password.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    form_class = ForgotPasswordForm

class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/reset_password.html'
    form_class = ResetPasswordForm