from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tour, TourStep
from .serializers import TourSerializer, TourStepSerializer

class TourViewSet(viewsets.ModelViewSet):
    serializer_class = TourSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Tour.objects.filter(creator=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_step(self, request, pk=None):
        tour = self.get_object()
        step_data = request.data
        step_data['tour'] = tour.id
        
        serializer = TourStepSerializer(data=step_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False)
    def dashboard_stats(self, request):
        user_tours = self.get_queryset()
        stats = {
            'total_tours': user_tours.count(),
            'published_tours': user_tours.filter(status='Published').count(),
            'total_views': sum(tour.view_count for tour in user_tours),
            'recent_tours': TourSerializer(user_tours[:5], many=True).data
        }
        return Response(stats)