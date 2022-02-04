# Generated by Django 3.1.4 on 2022-02-04 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_services', '0007_auto_20220203_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimeservice',
            name='service',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='one_time_service', to='hotel_services.service'),
        ),
    ]
