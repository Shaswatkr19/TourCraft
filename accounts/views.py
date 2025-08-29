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



def logout_view(request):
    """Logout user and redirect to login page"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

@csrf_protect
@never_cache
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
    
    return render(request, 'accounts/login.html')





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








# @login_required
# def settings_view(request):
#     """User settings view"""
#     user = request.user
    
#     if request.method == 'POST':
#         action = request.POST.get('action')
        
#         if action == 'update_profile':
#             user.first_name = request.POST.get('first_name', user.first_name)
#             user.last_name = request.POST.get('last_name', user.last_name)
#             user.email = request.POST.get('email', user.email)
            
#             try:
#                 user.save()
#                 messages.success(request, 'Profile updated successfully!')
#             except Exception as e:
#                 messages.error(request, 'Error updating profile.')
        
#         elif action == 'change_password':
#             current_password = request.POST.get('current_password')
#             new_password = request.POST.get('new_password')
#             confirm_password = request.POST.get('confirm_password')
            
#             if not user.check_password(current_password):
#                 messages.error(request, 'Current password is incorrect.')
#             elif new_password != confirm_password:
#                 messages.error(request, 'New passwords do not match.')
#             elif len(new_password) < 8:
#                 messages.error(request, 'Password must be at least 8 characters long.')
#             else:
#                 user.set_password(new_password)
#                 user.save()
#                 messages.success(request, 'Password changed successfully! Please login again.')
#                 return redirect('accounts:login')
        
#         return redirect('accounts:settings')
    
#     # User account stats
#     account_stats = {
#         'member_since': user.date_joined,
#         'last_login': user.last_login,
#         'tours_created': 5,  # Mock data
#         'storage_used': '2.3 MB',  # Mock data
#     }
    
#     context = {
#         'user': user,
#         'account_stats': account_stats
#     }
#     return render(request, 'accounts/settings.html', context)



# accounts/views.py mein ye function add karo
# @login_required
# def create_enhanced_tour(request):
#     """Enhanced tour creation dashboard"""
#     context = {
#         'user': request.user,
#         'title': 'Enhanced Tour Creation Dashboard'
#     }
#     return render(request, 'tours/preview_enhanced_v2.html', context)

# # tours_list_view bhi add karo
# @login_required
# def tours_list_view(request):
#     """Tours list view"""
#     context = {
#         'user': request.user,
#         'tours': []  # Empty for now
#     }
#     return render(request, 'tours/list.html', context)

