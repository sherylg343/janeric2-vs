# Generated by Django 3.1.5 on 2021-01-13 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20210109_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='marketing',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
