# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-26 22:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0081_quota_cached_availability_paid_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceaddress',
            name='internal_reference',
            field=models.TextField(blank=True, help_text='This reference will be printed on your invoice for your convenience.', verbose_name='Internal reference'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='internal_reference',
            field=models.TextField(blank=True),
        ),
    ]
