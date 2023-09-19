from django.core.cache import cache
from django.db.models import Prefetch, Count
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Test, Scores
from .serializers import TestSerializer


class TestListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Test.objects.filter(status__is_active=True).prefetch_related(
        Prefetch('scores', queryset=Scores.objects.all().select_related(
            'indicator_metric',
            'indicator_metric__metric',
            'indicator_metric__indicator',
            'indicator_metric__references'))
    )
    serializer_class = TestSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        test_cache_name = 'test_cache'
        test_cache = cache.get(test_cache_name)
        if test_cache:
            total_count_results = test_cache
        else:
            total_count_results = queryset.aggregate(total=Count('scores')).get('total')
            cache.set(test_cache_name, total_count_results, 30)

        response_data = {}
        response_data.update({'total_results': response.data})
        response_data.update({'count_results': total_count_results})
        response.data = response_data
        return response
