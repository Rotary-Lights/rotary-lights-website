# Generated by Django 5.0.7 on 2024-07-23 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0003_volunteeringcampaign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='address',
            field=models.CharField(max_length=150, verbose_name='Mailing Address'),
        ),
    ]
