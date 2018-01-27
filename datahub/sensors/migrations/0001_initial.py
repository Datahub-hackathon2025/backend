# Generated by Django 2.0.1 on 2018-01-27 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('datetime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Light',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('state_on', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('state_free', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('sensor_type', models.CharField(choices=[('temp', 'temp'), ('pollution', 'pollution'), ('electricity', 'electricity'), ('street_light', 'street_light'), ('parking_lot', 'parking_lot')], max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='datapoint',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sensors.Sensor'),
        ),
    ]
