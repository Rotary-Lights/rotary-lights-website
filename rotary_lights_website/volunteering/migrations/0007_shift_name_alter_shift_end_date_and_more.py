# Generated by Django 5.0.7 on 2024-08-01 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteering', '0006_rename_secondary_activity_organization_second_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='name',
            field=models.CharField(default='Any Weekend', max_length=255, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shift',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start Date'),
        ),
    ]
