# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2019-03-29 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Critic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_website', models.CharField(max_length=500)),
                ('name', models.CharField(max_length=50)),
                ('time', models.CharField(max_length=50)),
                ('link_website', models.CharField(max_length=500)),
            ],
        ),
    ]
