# Generated by Django 3.2.4 on 2021-07-12 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coloring', '0002_picture_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='Palette',
            fields=[
                ('name', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('colors', models.CharField(max_length=2000)),
            ],
        ),
    ]
