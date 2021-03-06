# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 05:57
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('okcupid', '0003_auto_20170519_1752'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Gender',
            new_name='Orientation',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='liked_genders',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='liked_orientation',
            field=models.ManyToManyField(related_name='_userprofile_liked_orientation_+', to='okcupid.Orientation'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='orientation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='okcupid.Orientation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1),
        ),
    ]
