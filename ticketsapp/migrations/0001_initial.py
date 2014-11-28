# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('due_date', models.DateTimeField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=12, null=True, blank=True)),
                ('progress_report', models.TextField(null=True, blank=True)),
                ('finished', models.BooleanField(default=False)),
                ('client', models.ForeignKey(related_name='client_tickets', to=settings.AUTH_USER_MODEL)),
                ('consultant', models.ForeignKey(related_name='consultant_tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
