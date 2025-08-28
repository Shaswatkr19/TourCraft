# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()  # This gets your custom User model

@csrf_protect
@never_cache

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def login_view(request):
    """Main login view"""
    print("🚀 Login view called!")  # Debug
    
    if request.user.is_authenticated and not request.GET.get('next'):
        print("👤 User already authenticated, redirecting to dashboard")
        return redirect('/tours/create/enhanced/')
    
    if request.method == 'POST':
        print("📝 POST request received!")  # Debug
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f"Username: {username}, Password: {password[:3]}***")  # Debug (partial password)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("✅ Authentication successful!")
            login(request, user)
            return redirect('/tours/create/enhanced/')  # Dashboard redirect
        else:
            print("❌ Authentication failed!")
            messages.error(request, 'Invalid username or password')
    else:
        print("📄 GET request - showing login page")
    
    return render(request, 'base/landing_simple.html')

@login_required
def dashboard_view(request):
    """Dashboard with mock data"""
    stats = {
        "tours": 6,
        "drafts": 2,
        "views": 1824,
        "shares": 97,
        "conversion": 12.4,
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
        "user": request.user,
    }
    return render(request, "accounts/dashboard.html", context)

def logout_view(request):
    """Logout user and redirect to login page"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

def signup_view(request):
    """Signup view for new users"""
    if request.user.is_authenticated:
        return redirect('/tours/create/enhanced/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'accounts/signup.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
    
    return render(request, 'accounts/signup.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username') or email.split('@')[0]  # Generate username from email
        
        # Validation
        if not all([email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
        elif User.objects.filter(username=username).exists():
            # Generate unique username if exists
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
        
        if not messages.get_messages(request):
            try:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Auto login after registration
                login(request, user)
                messages.success(request, f'Welcome to TourCraft, {user.first_name or user.username}!')
                return redirect('accounts:dashboard')
                
            except Exception as e:
                messages.error(request, 'Error creating account. Please try again.')
    
    return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    """User profile view with stats and update functionality"""
    user = request.user
    
    # Handle POST request for profile updates
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        try:
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
        except Exception as e:
            messages.error(request, 'Error updating profile. Please try again.')
    
    # Mock stats for now (replace with real data when Tour model exists)
    profile_data = {
        'user': user,
        'tours_created': 5,  # Mock data
        'total_views': 128,  # Mock data
        'published_tours': 3,  # Mock data
        'recent_tours': [],  # Empty for now
        'member_since': user.date_joined,
    }
    
    return render(request, 'accounts/profile.html', {
        'profile_data': profile_data
    })


@login_required
def analytics_view(request):
    """Analytics dashboard with mock data"""
    user = request.user
    
    # Mock analytics data
    analytics_data = {
        'total_tours': 8,
        'total_views': 1247,
        'completion_rate': 78,
        'avg_completion_time': '2.5 minutes',
        'top_performing_tour': 'Product Demo',
        'monthly_views': [
            {'month': 'Jan', 'views': 145},
            {'month': 'Feb', 'views': 234},
            {'month': 'Mar', 'views': 189},
            {'month': 'Apr', 'views': 298},
            {'month': 'May', 'views': 381},
        ]
    }
    
    context = {
        'user': user,
        'analytics': analytics_data
    }
    return render(request, 'accounts/analytics.html', context)

@login_required  
def team_view(request):
    """Team collaboration view"""
    user = request.user
    
    # Mock team data
    teams_data = {
        'my_teams': [
            {'name': 'Marketing Team', 'members': 5, 'role': 'Admin', 'active_projects': 3},
            {'name': 'Product Team', 'members': 8, 'role': 'Member', 'active_projects': 2},
        ],
        'recent_team_activity': [
            {'user': 'John Doe', 'action': 'created new tour', 'time': '2 hours ago'},
            {'user': 'Jane Smith', 'action': 'updated template', 'time': '5 hours ago'},
        ]
    }
    
    context = {
        'user': user,
        'teams': teams_data
    }
    return render(request, 'accounts/team.html', context)

@login_required
def templates_view(request):
    """Templates management view"""
    user = request.user
    
    # Mock templates data
    templates_data = {
        'my_templates': [
            {'name': 'Product Onboarding', 'category': 'Onboarding', 'usage_count': 25, 'created': '2024-01-15'},
            {'name': 'Feature Walkthrough', 'category': 'Feature Tour', 'usage_count': 18, 'created': '2024-02-10'},
            {'name': 'User Guide', 'category': 'Help', 'usage_count': 12, 'created': '2024-03-05'},
        ],
        'popular_templates': [
            {'name': 'Getting Started', 'category': 'Onboarding', 'usage_count': 156},
            {'name': 'Dashboard Tour', 'category': 'Navigation', 'usage_count': 134},
        ]
    }
    
    context = {
        'user': user,
        'templates': templates_data
    }
    return render(request, 'accounts/templates.html', context)

@login_required
def settings_view(request):
    """User settings view"""
    user = request.user
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            
            try:
                user.save()
                messages.success(request, 'Profile updated successfully!')
            except Exception as e:
                messages.error(request, 'Error updating profile.')
        
        elif action == 'change_password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password changed successfully! Please login again.')
                return redirect('accounts:login')
        
        return redirect('accounts:settings')
    
    # User account stats
    account_stats = {
        'member_since': user.date_joined,
        'last_login': user.last_login,
        'tours_created': 5,  # Mock data
        'storage_used': '2.3 MB',  # Mock data
    }
    
    context = {
        'user': user,
        'account_stats': account_stats
    }
    return render(request, 'accounts/settings.html', context)


def landing_page(request):
    """Landing page view"""
    return render(request, 'index.html')

# accounts/views.py mein ye function add karo
@login_required
def create_enhanced_tour(request):
    """Enhanced tour creation dashboard"""
    context = {
        'user': request.user,
        'title': 'Enhanced Tour Creation Dashboard'
    }
    return render(request, 'tours/preview_enhanced_v2.html', context)

# tours_list_view bhi add karo
@login_required
def tours_list_view(request):
    """Tours list view"""
    context = {
        'user': request.user,
        'tours': []  # Empty for now
    }
    return render(request, 'tours/list.html', context)

