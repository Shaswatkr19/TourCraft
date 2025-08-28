from django.db import models
from django.contrib.auth import get_user_model
from tours.models import Tour

User = get_user_model()

class Analytics(models.Model):
    tour = models.OneToOneField(Tour, on_delete=models.CASCADE, related_name='analytics')
    total_views = models.IntegerField(default=0)
    unique_viewers = models.IntegerField(default=0)
    avg_completion_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created Tour'),
        ('updated', 'Updated Tour'), 
        ('published', 'Published Tour'),
        ('viewed', 'Viewed Tour'),
        ('deleted', 'Deleted Tour'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    @property 
    def time_ago(self):
        from django.utils import timezone
        diff = timezone.now() - self.timestamp
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        else:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"