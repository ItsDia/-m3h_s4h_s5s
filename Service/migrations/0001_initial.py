# Generated by Django 5.0.4 on 2024-05-24 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('cost', models.IntegerField()),
                ('input_concepts', models.ManyToManyField(related_name='input_services', to='Service.concept')),
                ('output_concepts', models.ManyToManyField(related_name='output_services', to='Service.concept')),
            ],
        ),
    ]
