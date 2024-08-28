# Generated by Django 4.2.10 on 2024-03-15 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pretixbase", "0257_item_default_price_not_null"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="organizer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="pretixbase.organizer",
            ),
        ),
        migrations.AddField(
            model_name="orderposition",
            name="organizer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_positions",
                to="pretixbase.organizer",
            ),
        ),
        migrations.AddConstraint(
            model_name="order",
            constraint=models.UniqueConstraint(
                fields=("organizer", "code"), name="order_organizer_code_uniq"
            ),
        ),
        migrations.AddConstraint(
            model_name="orderposition",
            constraint=models.UniqueConstraint(
                models.F("organizer"),
                models.F("secret"),
                name="orderposition_organizer_secret_uniq",
            ),
        ),
    ]
