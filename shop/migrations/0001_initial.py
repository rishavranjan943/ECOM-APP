# Generated by Django 5.0.2 on 2024-03-11 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('price', models.FloatField()),
                ('discount_price', models.FloatField()),
                ('category', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('image', models.CharField(max_length=300)),
            ],
        ),
    ]
