# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-13 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formfactory', '0005_added_enum_generic_relation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fieldchoice',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='fieldchoice',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
