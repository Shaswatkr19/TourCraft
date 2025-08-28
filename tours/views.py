from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from .models import Tour, TourStep, Recording
# from analytics.models import ActivityLog
import json
import uuid
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from .models import SavedTour, Tour
from django.template.loader import render_to_string


def home(request):
    return HttpResponse("Welcome to Tours Home")

def tour_list(request):
    return HttpResponse("List of all tours")

def tour_detail(request, id):
    return HttpResponse(f"Details of tour {id}")

@login_required
def tours_all_view(request):
    """Display all tours for the current user"""
    tours = Tour.objects.filter(creator=request.user).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        tours = tours.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        tours = tours.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(tours, 12)  # 12 tours per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tours': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'page_obj': page_obj,
        'total_tours': tours.count(),
    }
    return render(request, 'tours/all.html', context)

@login_required
def dashboard_view(request):
    # Get user's tours
    tours = Tour.objects.filter(creator=request.user)
    
    # Get stats
    total_tours = tours.count()
    total_views = sum(tour.view_count for tour in tours)
    published_tours = tours.filter(status='Published').count()
    
    # Get recent activities - temporarily disabled
    # recent_activities = ActivityLog.objects.filter(user=request.user)[:5]
    recent_activities = []  # Empty list for now
    
    recent_tours = tours.order_by('-created_at')[:5]

    # Mock data for template compatibility
    stats = {
        'tours': total_tours,
        'views': f"{total_views/1000:.1f}k" if total_views > 1000 else str(total_views),
        'conversion': 87,  # Mock data
        'avg_time': '3.2m'  # Mock data
    }
    
    context = {
        'tours': tours,
        'stats': stats,
        'recent': recent_activities,
        'published_tours': published_tours,
        'recent_tours': recent_tours, 
    }
    return render(request, 'accounts/dashboard.html', context)

# Tours List View (renamed for consistency)
@login_required
def tours_list_view(request):
    tours = Tour.objects.filter(creator=request.user).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        tours = tours.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        tours = tours.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(tours, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tours': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'page_obj': page_obj,
    }
    return render(request, 'tours/list.html', context)

@login_required
def tour_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        privacy = request.POST.get('privacy', 'public')
        
        tour = Tour.objects.create(
            title=title,
            description=description,
            privacy=privacy,
            creator=request.user
        )
        
        # Log activity - temporarily disabled
        # ActivityLog.objects.create(
        #     user=request.user,
        #     tour=tour,
        #     action='created'
        # )
        
        messages.success(request, 'Tour created successfully!')
        return redirect('tour_detail', pk=tour.id)
    
    return render(request, 'tours/create.html')

@login_required
def tour_detail_view(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    steps = tour.steps.all().order_by('order')
    
    context = {
        'tour': tour,
        'steps': steps,
        'total_steps': steps.count(),
    }
    return render(request, 'tours/detail.html', context)

@login_required
def tour_edit_view(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    
    if request.method == 'POST':
        tour.title = request.POST.get('title', tour.title)
        tour.description = request.POST.get('description', tour.description)
        tour.privacy = request.POST.get('privacy', tour.privacy)
        tour.status = request.POST.get('status', tour.status)
        tour.updated_at = timezone.now()
        tour.save()
        
        messages.success(request, 'Tour updated successfully!')
        return redirect('tour_detail', pk=tour.id)
    
    context = {
        'tour': tour,
    }
    return render(request, 'tours/edit.html', context)

@login_required
def tour_delete_view(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    
    if request.method == 'POST':
        tour_title = tour.title
        tour.delete()
        messages.success(request, f'Tour "{tour_title}" deleted successfully!')
        return redirect('tours_list')
    
    context = {
        'tour': tour,
    }
    return render(request, 'tours/delete.html', context)

@login_required
def tour_duplicate_view(request, pk):
    original_tour = get_object_or_404(Tour, id=pk, creator=request.user)
    
    # Create duplicate
    new_tour = Tour.objects.create(
        title=f"{original_tour.title} (Copy)",
        description=original_tour.description,
        privacy=original_tour.privacy,
        creator=request.user,
        status='Draft'
    )
    
    # Copy steps
    for step in original_tour.steps.all():
        TourStep.objects.create(
            tour=new_tour,
            title=step.title,
            content=step.content,
            element_selector=step.element_selector,
            order=step.order,
            step_type=step.step_type
        )
    
    messages.success(request, f'Tour duplicated as "{new_tour.title}"!')
    return redirect('tour_detail', pk=new_tour.id)

# Tour Steps Management
@login_required
def tour_steps_view(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    steps = tour.steps.all().order_by('order')
    
    context = {
        'tour': tour,
        'steps': steps,
    }
    return render(request, 'tours/steps.html', context)

@login_required
def step_create_view(request, tour_pk):
    tour = get_object_or_404(Tour, id=tour_pk, creator=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        element_selector = request.POST.get('element_selector')
        step_type = request.POST.get('step_type', 'tooltip')
        
        # Get next order number
        max_order = tour.steps.aggregate(max_order=Count('order'))['max_order'] or 0
        
        step = TourStep.objects.create(
            tour=tour,
            title=title,
            content=content,
            element_selector=element_selector,
            step_type=step_type,
            order=max_order + 1
        )
        
        messages.success(request, 'Step added successfully!')
        return redirect('tour_steps', pk=tour.id)
    
    context = {
        'tour': tour,
    }
    return render(request, 'tours/step_create.html', context)

@login_required
def step_edit_view(request, tour_pk, step_pk):
    tour = get_object_or_404(Tour, id=tour_pk, creator=request.user)
    step = get_object_or_404(TourStep, id=step_pk, tour=tour)
    
    if request.method == 'POST':
        step.title = request.POST.get('title', step.title)
        step.content = request.POST.get('content', step.content)
        step.element_selector = request.POST.get('element_selector', step.element_selector)
        step.step_type = request.POST.get('step_type', step.step_type)
        step.save()
        
        messages.success(request, 'Step updated successfully!')
        return redirect('tour_steps', pk=tour.id)
    
    context = {
        'tour': tour,
        'step': step,
    }
    return render(request, 'tours/step_edit.html', context)

@login_required
def step_delete_view(request, tour_pk, step_pk):
    tour = get_object_or_404(Tour, id=tour_pk, creator=request.user)
    step = get_object_or_404(TourStep, id=step_pk, tour=tour)
    
    if request.method == 'POST':
        step.delete()
        messages.success(request, 'Step deleted successfully!')
        return redirect('tour_steps', pk=tour.id)
    
    context = {
        'tour': tour,
        'step': step,
    }
    return render(request, 'tours/step_delete.html', context)

# Public tour viewing (no login required)
def tour_public_view(request, tour_uuid):
    tour = get_object_or_404(Tour, public_uuid=tour_uuid, privacy='public', status='Published')
    steps = tour.steps.all().order_by('order')
    
    # Increment view count
    tour.view_count += 1
    tour.save()
    
    context = {
        'tour': tour,
        'steps': steps,
        'is_public_view': True,
    }
    return render(request, 'tours/public_view.html', context)

# API endpoint for tour data (for JavaScript integration)
@login_required
def tour_api_data(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    steps = tour.steps.all().order_by('order')
    
    tour_data = {
        'id': tour.id,
        'title': tour.title,
        'description': tour.description,
        'steps': [
            {
                'id': step.id,
                'title': step.title,
                'content': step.content,
                'element_selector': step.element_selector,
                'step_type': step.step_type,
                'order': step.order,
            }
            for step in steps
        ]
    }
    
    return JsonResponse(tour_data)

# Tour analytics view
@login_required
def tour_analytics_view(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    
    # Mock analytics data (replace with real analytics later)
    analytics_data = {
        'total_views': tour.view_count,
        'completion_rate': 75,  # Mock data
        'avg_time_spent': '2.5 minutes',  # Mock data
        'bounce_rate': 25,  # Mock data
        'daily_views': [10, 15, 8, 22, 18, 25, 30],  # Mock weekly data
    }
    
    context = {
        'tour': tour,
        'analytics': analytics_data,
    }
    return render(request, 'tours/analytics.html', context)

# Tour preview (for testing)
@login_required
def tour_preview_view(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    steps = tour.steps.all().order_by('order')
    
    context = {
        'tour': tour,
        'steps': steps,
        'is_preview': True,
    }
    return render(request, 'tours/preview.html', context)

# Tour sharing/embed
@login_required
def tour_share_view(request, pk):
    tour = get_object_or_404(Tour, id=pk, creator=request.user)
    
    # Generate public UUID if not exists
    if not tour.public_uuid:
        tour.public_uuid = str(uuid.uuid4())
        tour.save()
    
    context = {
        'tour': tour,
        'public_url': request.build_absolute_uri(f'/public/tour/{tour.public_uuid}/'),
        'embed_code': f'<iframe src="{request.build_absolute_uri(f"/public/tour/{tour.public_uuid}/")}" width="100%" height="400"></iframe>',
    }
    return render(request, 'tours/share.html', context)

def tour_create_enhanced_view(request):
    """Enhanced tour creation view with visual editor"""
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        description = request.POST.get('description')
        privacy = request.POST.get('privacy', 'private')
        status = request.POST.get('status', 'Draft')
        
        tour = Tour.objects.create(
            title=title,
            description=description,
            privacy=privacy,
            status=status,
            creator=request.user
        )
        
        messages.success(request, f'Tour "{title}" created successfully!')
        return redirect('tours:tour_steps', pk=tour.pk)
    
    return render(request, 'tours/create_enhanced.html')

def tour_preview_enhanced_view(request, pk):
    """Enhanced tour preview with interactive player"""
    tour = get_object_or_404(Tour, pk=pk)
    steps = tour.steps.all().order_by('step_number')
    
    # Convert steps to JSON for JavaScript
    steps_data = []
    for step in steps:
        step_data = {
            'id': step.id,
            'title': step.title,
            'description': step.description,
            'screenshot': step.screenshot.url if step.screenshot else None,
            'highlight_area': step.highlight_area,
            'recording': {
                'duration': step.recording.duration if hasattr(step, 'recording') and step.recording else 0
            } if hasattr(step, 'recording') and step.recording else None
        }
        steps_data.append(step_data)
    
    context = {
        'tour': tour,
        'steps': steps_data,
    }
    return render(request, 'tours/preview_enhanced.html', context)

def tour_preview_enhanced_v2_view(request, pk):
    """Enhanced tour preview v2 with interactive step-by-step navigation"""
    tour = get_object_or_404(Tour, pk=pk)
    steps = tour.steps.all().order_by('step_number')
    
    # Convert steps to JSON for JavaScript
    steps_data = []
    for step in steps:
        step_data = {
            'id': step.id,
            'title': step.title,
            'description': step.description,
            'screenshot': step.screenshot.url if step.screenshot else None,
            'highlight_area': step.highlight_area,
            'recording': {
                'duration': step.recording.duration if hasattr(step, 'recording') and step.recording else 0
            } if hasattr(step, 'recording') and step.recording else None
        }
        steps_data.append(step_data)
    
    context = {
        'tour': tour,
        'steps': steps_data,
    }
    return render(request, 'tours/preview_enhanced_v2.html', context)

@login_required
def saved_tours_view(request):
    saved_tours = SavedTour.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tours/saved_tours.html', {'saved_tours': saved_tours})