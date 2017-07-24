# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 19:01
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ClientUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Functionality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable_probability', models.DecimalField(decimal_places=6, default=Decimal('0'), max_digits=7)),
                ('color', models.CharField(default=b'c0ffee', max_length=6)),
                ('client_users', models.ManyToManyField(through='core.Availability', to='core.ClientUser')),
            ],
        ),
        migrations.CreateModel(
            name='FunctionalityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='functionality',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.FunctionalityGroup'),
        ),
        migrations.AddField(
            model_name='availability',
            name='functionality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Functionality'),
        ),
        migrations.AddField(
            model_name='availability',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ClientUser'),
        ),
    ]
