# Generated by Django 5.1.3 on 2024-12-31 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EMUSIC_Application', '0011_alter_customuser_mailid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='additional_field',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]