# Generated by Django 3.2.9 on 2021-11-12 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BattleZone', '0002_auto_20211112_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalinfo',
            name='Occupation',
            field=models.CharField(choices=[('STU', 'Student'), ('PRO', 'Professional'), ('OTR', 'Other')], max_length=3),
        ),
    ]
