# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketsapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='finished',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True, auto_created=True),
            preserve_default=True,
        ),
    ]
