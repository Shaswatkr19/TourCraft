# tours/serializers.py
from rest_framework import serializers
from .models import Tour, TourStep

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['id', 'title', 'description', 'status', 'creator', 'view_count', 'created_at', 'updated_at']
        read_only_fields = ['creator', 'view_count', 'created_at', 'updated_at']

class TourStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourStep
        fields = ['id', 'tour', 'title', 'content', 'order', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']