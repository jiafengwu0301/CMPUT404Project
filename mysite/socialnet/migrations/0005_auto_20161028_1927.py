# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialnet', '0004_auto_20161024_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.ImageField(upload_to=b'C:\\Users\\Gustavo\\Documents\\GitHub\\CMPUT404Project\\mysite\\static'),
        ),
    ]
