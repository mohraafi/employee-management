# Generated by Django 4.2.7 on 2023-12-07 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
