# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-20 05:52
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('okcupid', '0002_auto_20170511_0023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.DateTimeField(auto_created=True)),
                ('text', models.CharField(max_length=600)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SendedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250)),
                ('accepted', models.NullBooleanField(default=None)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='min_match',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sendedquestion',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='okcupid.UserProfile'),
        ),
        migrations.AddField(
            model_name='opinion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='okcupid.UserProfile'),
        ),
        migrations.AddField(
            model_name='message',
            name='from_u',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='okcupid.UserProfile'),
        ),
        migrations.AddField(
            model_name='message',
            name='to_u',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='okcupid.UserProfile'),
        ),
    ]
