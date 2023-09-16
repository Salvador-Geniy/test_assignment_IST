from django.contrib import admin

from .models import (Status, Laboratory, Test,
                            Indicator, Metric, IndicatorMetric,
                            Scores, References)

my_models = [
    Status, Laboratory, Test,
    Indicator, Metric, IndicatorMetric,
    Scores, References
]

admin.site.register(my_models)

