# Generated by Django 4.2 on 2025-03-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_order_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.TextField(blank=True, default=''),
        ),
    ]
