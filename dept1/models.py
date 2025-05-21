from django.db import models

class ChartData(models.Model):
    # category = models.CharField(max_length=100)
    # value = models.IntegerField()
    # chart_type = models.CharField(max_length=50)  # pie, bar, etc.
    username = models.CharField(max_length=50, default='anonymous')  # User who created the entry
    preferred_category = models.CharField(max_length=100, blank=True)  # Optional preferred category

    def __str__(self):
        return f" {self.username} - {self.preferred_category}"