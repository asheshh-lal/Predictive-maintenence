# Generated by Django 5.0.3 on 2024-03-28 15:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dash",
            name="Air_temperature",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="dash",
            name="Process_temperature",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="dash",
            name="Torque_Nm",
            field=models.FloatField(default=0),
        ),
    ]