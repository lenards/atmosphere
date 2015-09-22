# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_machinerequest_new_version_scripts'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdentityMembershipHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_name', models.CharField(max_length=255)),
                ('operation', models.CharField(default=b'UPDATE', max_length=255, choices=[(b'CREATE', b'The field has been created.'), (b'UPDATE', b'The field has been updated.'), (b'DELETED', b'The field has been deleted.')])),
                ('current_value', models.TextField()),
                ('previous_value', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('membership', models.ForeignKey(related_name='history', to='core.IdentityMembership')),
            ],
            options={
                'db_table': 'identity_membership_history',
            },
        ),
    ]
