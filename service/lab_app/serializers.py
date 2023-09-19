from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Test, Scores


class ScoreSerializer(ModelSerializer):
    indicator_name = serializers.CharField(source='indicator_metric.indicator.name')
    metric_name = serializers.CharField(source='indicator_metric.metric.metric_name')
    metric_unit = serializers.CharField(source='indicator_metric.metric.unit')
    is_within_normal_range = serializers.SerializerMethodField()

    class Meta:
        model = Scores
        fields = ('id', 'score', 'indicator_name', 'metric_name',
                  'metric_unit', 'is_within_normal_range')

    def get_is_within_normal_range(self, instance):
        min = instance.indicator_metric.references.min_score
        max = instance.indicator_metric.references.max_score
        return min <= instance.score <= max


class TestSerializer(ModelSerializer):
    duration = serializers.SerializerMethodField()
    results = ScoreSerializer(source='scores', many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'laboratory', 'duration', 'results')

    def get_duration(self, instance):
        return (instance.completed_at - instance.started_at)
