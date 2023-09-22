from django.conf import settings
from django.core.cache import cache
from django.db import models
import uuid

from django.db.models.signals import post_delete

from .receivers import delete_cache_test_cache


class Status(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'


class Laboratory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    status = models.OneToOneField(Status, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'laboratory'
        verbose_name_plural = 'laboratories'


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField()
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)
        if creating:
            cache.delete(settings.TEST_CACHE_NAME)
        return result


class Indicator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.OneToOneField(Status, on_delete=models.PROTECT)


class Metric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    metric_name = models.CharField(max_length=255)
    description = models.TextField()
    unit = models.CharField(max_length=255)
    status = models.OneToOneField(Status, on_delete=models.PROTECT)


class IndicatorMetric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='indicator_metric')
    metric = models.OneToOneField(Metric, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.PROTECT)


class Scores(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    score = models.DecimalField(max_digits=15, decimal_places=5)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='scores')
    indicator_metric = models.OneToOneField(IndicatorMetric, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'scores'
        verbose_name_plural = 'scores'


class References(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    min_score = models.DecimalField(max_digits=15, decimal_places=5)
    max_score = models.DecimalField(max_digits=15, decimal_places=5)
    indicator_metric = models.OneToOneField(IndicatorMetric, on_delete=models.CASCADE)
    status = models.OneToOneField(Status, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'references'
        verbose_name_plural = 'references'


post_delete.connect(delete_cache_test_cache, sender=Test)
post_delete.connect(delete_cache_test_cache, sender=Scores)
