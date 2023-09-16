
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView

from .models import Test
from .serializers import TestSerializer


class TestListView(ListAPIView):
    queryset = Test.objects.filter(status__is_active=True).prefetch_related(Prefetch('scores')).order_by('laboratory')
    serializer_class = TestSerializer
