# Generated by Django 4.2.16 on 2024-12-25 20:16

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_correctanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]
