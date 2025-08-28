from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
import uuid


class Tour(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Archived', 'Archived'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tours"
    )
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default="public")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Draft")
    thumbnail = models.ImageField(upload_to="tour_thumbnails/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["privacy"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"

    @property
    def steps_count(self):
        return self.steps.count()

    @property
    def updated_ago(self):
        diff = timezone.now() - self.updated_at
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        return f"{diff.seconds // 60} minutes ago"

    def is_published(self):
        return self.status == "Published"


class TourStep(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="steps")
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    screenshot = models.ImageField(upload_to="tour_steps/", blank=True, null=True)
    highlight_area = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["step_number"]
        constraints = [
            models.UniqueConstraint(fields=["tour", "step_number"], name="unique_step_per_tour")
        ]

    def __str__(self):
        return f"{self.tour.title} - Step {self.step_number}: {self.title}"


class SavedTour(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file_url = models.FileField(upload_to='saved_tours/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Recording(models.Model):
    STATUS_CHOICES = [
        ("recording", "Recording"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recordings"
    )
    title = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="recording")
    recording_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Recording {self.title or self.id} ({self.status})"

    @property
    def duration(self):
        if self.completed_at:
            return (self.completed_at - self.created_at).total_seconds()
        return None


class TourView(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="views")
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tour", "viewer", "ip_address"], name="unique_view_per_user")
        ]
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"View on {self.tour.title} by {self.viewer or self.ip_address}"