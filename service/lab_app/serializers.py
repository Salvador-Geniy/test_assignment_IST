from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Test, Scores


class ScoreSerializer(ModelSerializer):

    class Meta:
        model = Scores
        fields = ('id', 'score')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        min = instance.indicator_metric.references.min_score
        max = instance.indicator_metric.references.max_score

        representation['indicator_name'] = instance.indicator_metric.indicator.name
        representation['metric_name'] = instance.indicator_metric.metric.metric_name
        representation['metric_unit'] = instance.indicator_metric.metric.unit
        representation['is_within_normal_range'] = min <= instance.score <= max

        return representation


class TestSerializer(ModelSerializer):
    duration = serializers.SerializerMethodField()
    results = ScoreSerializer(source='scores', many=True, read_only=True)

    class Meta:
        model = Test
        fields = ('id', 'laboratory', 'duration', 'results')

    def get_duration(self, obj):
        return (obj.completed_at - obj.started_at)
