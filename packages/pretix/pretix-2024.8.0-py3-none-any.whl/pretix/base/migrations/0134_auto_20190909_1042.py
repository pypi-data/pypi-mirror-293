# Generated by Django 2.2.4 on 2019-09-09 10:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import pretix.base.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0133_auto_20190830_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebAuthnDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('confirmed', models.BooleanField(default=True)),
                ('credential_id', models.CharField(max_length=255, null=True)),
                ('rp_id', models.CharField(max_length=255, null=True)),
                ('icon_url', models.CharField(max_length=255, null=True)),
                ('ukey', models.TextField(null=True)),
                ('pub_key', models.TextField(null=True)),
                ('sign_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
