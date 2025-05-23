# Generated by Django 5.2.1 on 2025-05-21 10:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dept1', '0003_remove_chartdata_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartdata',
            name='username',
            field=models.CharField(help_text='Required. 50 characters or fewer. Letters, numbers and underscores only.', max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username must contain only letters, numbers, and underscores', regex='^[a-zA-Z0-9_]+$')]),
        ),
        migrations.AddConstraint(
            model_name='chartdata',
            constraint=models.UniqueConstraint(condition=models.Q(('username', 'anonymous'), _negated=True), fields=('username',), name='unique_non_anonymous_username'),
        ),
    ]
