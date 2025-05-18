from django.db import models

class ChartData(models.Model):
    category = models.CharField(max_length=100)
    value = models.IntegerField()
    chart_type = models.CharField(max_length=50)  # pie, bar, etc.

    def __str__(self):
        return f"{self.category}: {self.value} ({self.chart_type})"