# Generated by Django 5.1.3 on 2025-01-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMUSIC_Application', '0012_customuser_additional_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='subscriptionplan',
            name='features',
            field=models.TextField(default='Standard features included.'),
        ),
    ]