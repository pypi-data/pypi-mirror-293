# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-28 12:17
from __future__ import unicode_literals

from django.db import migrations, models

import pretix.base.models.items


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0087_auto_20180317_1952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staffsession',
            options={'ordering': ('date_start',)},
        ),
        migrations.AlterModelOptions(
            name='staffsessionauditlog',
            options={'ordering': ('datetime',)},
        ),
        migrations.AlterField(
            model_name='item',
            name='picture',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=pretix.base.models.items.itempicture_upload_to, verbose_name='Product picture'),
        ),
    ]
