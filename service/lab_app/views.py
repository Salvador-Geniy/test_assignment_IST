
from django.db.models import Prefetch
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
