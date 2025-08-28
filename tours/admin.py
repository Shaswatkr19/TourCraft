from django.contrib import admin
from .models import Tour, TourStep, Recording, TourView


class TourStepInline(admin.TabularInline):
    model = TourStep
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "creator", "privacy", "status", "view_count", "created_at", "updated_at")
    list_filter = ("privacy", "status", "created_at")
    search_fields = ("title", "creator__email", "creator__username")
    inlines = [TourStepInline]


@admin.register(TourStep)
class TourStepAdmin(admin.ModelAdmin):
    list_display = ("tour", "step_number", "title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "tour__title")


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "created_at", "completed_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "user__email", "user__username")


@admin.register(TourView)
class TourViewAdmin(admin.ModelAdmin):
    list_display = ("tour", "viewer", "ip_address", "viewed_at")
    list_filter = ("viewed_at",)
    search_fields = ("tour__title", "viewer__email", "ip_address")

 
