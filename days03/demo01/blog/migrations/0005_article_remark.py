# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-15 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20181013_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='remark',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='摘要'),
        ),
    ]
