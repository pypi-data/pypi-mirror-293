# Generated by Django 4.2.10 on 2024-04-02 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pretixbase", "0259_team_require_2fa"),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name="reusablemedium",
            index_together=set(),
        ),
    ]
