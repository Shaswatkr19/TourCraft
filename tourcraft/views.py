from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.core.mail import EmailMessage

@login_required
def dashboard_view(request):
    """Dashboard view with mocked data"""
    
    # ---- mocked data so template never errors ----
    stats = {
        "tours": 6,
        "drafts": 2,
        "views": 1824,
        "shares": 97,
        "conversion": 12.4,  # %
        "avg_time": "01:42",
    }

    tours = [
        {"title": "Onboarding Flow", "status": "Published", "updated": "Aug 20, 2025"},
        {"title": "New Billing UI", "status": "Draft", "updated": "Aug 18, 2025"},
        {"title": "Feature: Smart Tours", "status": "Published", "updated": "Aug 14, 2025"},
    ]

    recent = [
        {"who": "You", "what": "Edited tour", "target": "New Billing UI", "when": "2h ago"},
        {"who": "Aditi", "what": "Published tour", "target": "Smart Tours", "when": "Yesterday"},
        {"who": "Rohan", "what": "Commented", "target": "Onboarding Flow", "when": "2 days ago"},
    ]

    context = {
        "stats": stats,
        "tours": tours,
        "recent": recent,
        "user": request.user,  # Add user info for template
    }
    return render(request, "accounts/dashboard.html", context)

def logout_view(request):
    """Logout user and redirect to login page"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def signup_view(request):
    """Signup view for new users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'registration/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'registration/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'registration/signup.html')
        
        # Create new user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
    
    return render(request, 'accounts/signup.html')


@login_required(login_url='/accounts/login/')
def create_enhanced_tour(request):
    context = {}
    # Your view logic here
    if request.method == 'POST':
        # Handle POST request
        pass
    else:
        # Handle GET request
        pass
    
    return render(request, 'your_template.html', context)

def home_view(request):
    """Main landing/home page"""
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard/')
    return render(request, 'base/landing_simple.html')

# Enhanced tour creation - requires login
@login_required(login_url='/accounts/login/')
def create_enhanced_tour(request):
    """Enhanced tour creation dashboard"""
    context = {
        'user': request.user,
        'title': 'Enhanced Tour Creation'
    }
    return render(request, 'preview_enhanced_v2.html', context)

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('tourcraft:password_reset_done')  # namespace ke saath
    email_template_name = 'registration/password_reset_email.html'

    def form_valid(self, form):
        # user email
        email = form.cleaned_data["email"]

        # custom email content (optional override)
        subject = "🔑 Password Reset Request - TourCraft"
        body = "Hello,\n\nPlease click the link to reset your password.\n\nThanks!"
        from_email = 'TourCraft <shaswatsinha05@gmail.com>'  # fixed sender email

        msg = EmailMessage(subject, body, from_email, [email])
        try:
            msg.send(fail_silently=False)
            messages.success(self.request, "✅ Reset email sent successfully! Check your inbox.")
        except Exception as e:
            messages.error(self.request, "❌ Failed to send reset email. Please try again.")
            print("Password reset mail error:", e)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "❌ Invalid form submission. Please try again.")
        return super().form_invalid(form)


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('tourcraft:password_reset_complete')


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'