from django.test import TestCase
from lab_app.models import (Status, Laboratory, Indicator,
                                    Test, Metric, IndicatorMetric, Scores, References)
from lab_app.serializers import TestSerializer, ScoreSerializer
import datetime


class ScoreSerializerTestCase(TestCase):
    def test_ok(self):
        statuses = [Status.objects.create() for _ in range(7)]
        laboratory = Laboratory.objects.create(name='Test Lab', status=statuses[0])
        test = Test.objects.create(started_at=datetime.datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                   completed_at=datetime.datetime.strptime('2023-01-01 00:00:10', '%Y-%m-%d %H:%M:%S'),
                                   laboratory=laboratory,
                                   status=statuses[1])
        indicator = Indicator.objects.create(name='Indicator',
                                             description='Test Indicator description',
                                             status=statuses[2])
        metric = Metric.objects.create(metric_name='Metric',
                                       description='Metric description',
                                       unit='sec',
                                       status=statuses[3])
        indicator_metric = IndicatorMetric.objects.create(indicator=indicator,
                                                          metric=metric,
                                                          status=statuses[4])
        scores = Scores.objects.create(score=12.00,
                                       test=test,
                                       indicator_metric=indicator_metric,
                                       status=statuses[5])
        references = References.objects.create(min_score=10.00,
                                               max_score=20.00,
                                               indicator_metric=indicator_metric,
                                               status=statuses[6])
        data = ScoreSerializer(scores).data
        expected_data = {
            'id': str(scores.id),
            'score': '12.00000',
            'indicator_name': 'Indicator',
            'metric_name': 'Metric',
            'metric_unit': 'sec',
            'is_within_normal_range': True
        }
        self.assertEqual(expected_data, data)


class TestSerializerTestCase(TestCase):
    def test_ok(self):
        statuses = [Status.objects.create() for _ in range(11)]
        laboratory = Laboratory.objects.create(name='Test Lab', status=statuses[0])
        test = Test.objects.create(started_at=datetime.datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                   completed_at=datetime.datetime.strptime('2023-01-01 00:00:10', '%Y-%m-%d %H:%M:%S'),
                                   laboratory=laboratory,
                                   status=statuses[1])
        indicator = Indicator.objects.create(name='Test Indicator',
                                             description='Test Indicator description',
                                             status=statuses[2])
        metric1 = Metric.objects.create(metric_name='Metric 1',
                                        description='Metric 1 description',
                                        unit='sec',
                                        status=statuses[3])
        metric2 = Metric.objects.create(metric_name='Metric 2',
                                        description='Metric 2 description',
                                        unit='%',
                                        status=statuses[4])
        indicator_metric1 = IndicatorMetric.objects.create(indicator=indicator,
                                                           metric=metric1,
                                                           status=statuses[5])
        indicator_metric2 = IndicatorMetric.objects.create(indicator=indicator,
                                                           metric=metric2,
                                                           status=statuses[6])
        scores1 = Scores.objects.create(score=12.00,
                                        test=test,
                                        indicator_metric=indicator_metric1,
                                        status=statuses[7])
        scores2 = Scores.objects.create(score=0.0055,
                                        test=test,
                                        indicator_metric=indicator_metric2,
                                        status=statuses[8])
        references1 = References.objects.create(min_score=10.00,
                                                max_score=20.00,
                                                indicator_metric=indicator_metric1,
                                                status=statuses[9])
        references2 = References.objects.create(min_score=1.00,
                                                max_score=20.00,
                                                indicator_metric=indicator_metric2,
                                                status=statuses[10])
        data = TestSerializer(test).data
        expected_data = {
            "id": str(test.id),
            "laboratory": laboratory.id,
            "duration": datetime.timedelta(seconds=10),
            "results": [
                {
                    "id": str(scores1.id),
                    "score": "12.00000",
                    "indicator_name": "Test Indicator",
                    "metric_name": "Metric 1",
                    "metric_unit": "sec",
                    "is_within_normal_range": True
                },
                {
                    "id": str(scores2.id),
                    "score": "0.00550",
                    "indicator_name": "Test Indicator",
                    "metric_name": "Metric 2",
                    "metric_unit": "%",
                    "is_within_normal_range": False
                }
            ]
        }

        self.assertEqual(expected_data, data)
