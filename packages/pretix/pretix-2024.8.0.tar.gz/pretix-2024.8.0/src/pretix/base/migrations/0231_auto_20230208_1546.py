# Generated by Django 3.2.17 on 2023-02-08 15:46

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0230_auto_20230208_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='validity_dynamic_duration_days',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_dynamic_duration_hours',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_dynamic_duration_minutes',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_dynamic_duration_months',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_dynamic_start_choice',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_dynamic_start_choice_day_limit',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_fixed_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_fixed_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='validity_mode',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='cartposition',
            name='requested_valid_from',
            field=models.DateTimeField(null=True),
        ),
    ]
