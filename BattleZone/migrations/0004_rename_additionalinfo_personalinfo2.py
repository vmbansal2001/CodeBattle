# Generated by Django 3.2.9 on 2021-11-12 07:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BattleZone', '0003_alter_additionalinfo_occupation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdditionalInfo',
            new_name='PersonalInfo2',
        ),
    ]