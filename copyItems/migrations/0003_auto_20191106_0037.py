# Generated by Django 2.2.6 on 2019-11-06 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copyItems', '0002_auto_20191105_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationdata',
            name='copy_item',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='publicationdata',
            name='video_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
