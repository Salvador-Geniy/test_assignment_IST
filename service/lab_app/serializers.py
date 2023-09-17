from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Test, Scores


class ScoreSerializer(ModelSerializer):
    indicator_name = serializers.SerializerMethodField()
    metric_name = serializers.SerializerMethodField()
    metric_unit = serializers.SerializerMethodField()
    is_within_normal_range = serializers.SerializerMethodField()

    class Meta:
        model = Scores
        fields = ('id', 'score', 'indicator_name', 'metric_name',
                  'metric_unit', 'is_within_normal_range')

    def get_indicator_name(self, obj):
        indicator_name = obj.indicator_metric.indicator.name
        return indicator_name

    def get_metric_name(self, obj):
        return obj.indicator_metric.metric.metric_name

    def get_metric_unit(self, obj):
        return obj.indicator_metric.metric.unit

    def get_is_within_normal_range(self, obj):
        min = obj.indicator_metric.references.min_score
        max = obj.indicator_metric.references.max_score
        return min <= obj.score <= max


class TestSerializer(ModelSerializer):
    duration = serializers.SerializerMethodField()
    results = ScoreSerializer(source='scores', many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'laboratory', 'duration', 'results')

    def get_duration(self, obj):
        return (obj.completed_at - obj.started_at)
