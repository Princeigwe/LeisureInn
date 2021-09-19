# Generated by Django 3.1.4 on 2021-09-14 22:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('SINGLE ROOM', 'Single Room'), ('DOUBLE ROOM', 'Double Room'), ('TRIPLE ROOM', 'Triple Room'), ('QUAD ROOM', 'Quad Room')], default='SINGLE ROOM', max_length=20)),
                ('first_item', models.CharField(blank=True, max_length=20)),
                ('second_item', models.CharField(blank=True, max_length=20)),
                ('third_item', models.CharField(blank=True, max_length=20)),
                ('fourth_item', models.CharField(blank=True, max_length=20)),
                ('fifth_item', models.CharField(blank=True, max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Amenities',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=3)),
                ('room_picture', models.ImageField(default='', upload_to='room_pictures/')),
                ('room_type', models.CharField(choices=[('SINGLE ROOM', 'Single Room'), ('DOUBLE ROOM', 'Double Room'), ('TRIPLE ROOM', 'Triple Room'), ('QUAD ROOM', 'Quad Room')], default='SINGLE ROOM', max_length=20)),
                ('is_available', models.BooleanField(default=True)),
                ('is_booked', models.BooleanField(default=False)),
                ('room_price', models.DecimalField(decimal_places=2, default='1000.00', max_digits=9)),
                ('amenities_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rooms.amenities')),
            ],
        ),
    ]
