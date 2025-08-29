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
    return render(request, 'tours/preview_enhanced_v2.html', context)




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

@login_required
def tour_list(request):
    tours = Tour.objects.filter(creator=request.user)
    return render(request, 'tours/steps.html', {'tours': tours})



@login_required
def EnhancedTourCreateView(request):
    """Enhanced tour creation dashboard"""
    context = {
        'user': request.user,
        'title': 'Enhanced Tour Creation Dashboard'
    }
    return render(request, 'tours/preview_enhanced_v2.html', context)

@login_required
def tour_create_view(request):
    """Basic tour creation view"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if title:
            tour = Tour.objects.create(
                title=title,
                description=description,
                creator=request.user,
                status='Draft'
            )
            messages.success(request, f'Tour "{title}" created successfully!')
            return redirect('tours:tour_steps', pk=tour.id)
        else:
            messages.error(request, 'Tour title is required.')
    
    context = {
        'title': 'Create New Tour'
    }
    return render(request, 'tours/tour_create.html', context)