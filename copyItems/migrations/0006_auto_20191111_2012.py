# Generated by Django 2.2.6 on 2019-11-11 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copyItems', '0005_auto_20191111_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='offset_query',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='publicationdata',
            name='copy',
            field=models.BooleanField(default=True),
        ),
    ]
