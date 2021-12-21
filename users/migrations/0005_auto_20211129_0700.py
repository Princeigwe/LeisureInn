# Generated by Django 3.1.4 on 2021-11-29 07:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='customuser',
            name='country',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='mobile',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='customuser',
            name='occupation',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
