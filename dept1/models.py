from django.db import models
from django.db.models import Q, UniqueConstraint
from django.core.validators import RegexValidator

class ChartData(models.Model):
    username = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9_]+$',
                message='Username must contain only letters, numbers, and underscores',
                code='invalid_username'
            ),
        ],
        help_text='Required. 50 characters or fewer. Letters, numbers and underscores only.'
    )
    preferred_category = models.CharField(max_length=100, blank=True)  # Optional preferred category

    def save(self, *args, **kwargs):
        self.preferred_category = self.preferred_category.upper()
        super().save(*args, **kwargs)


    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['username'],
                condition=~Q(username='anonymous'),
                name='unique_non_anonymous_username'
            )
        ]

    def __str__(self):
        return f" {self.username} - {self.preferred_category}"