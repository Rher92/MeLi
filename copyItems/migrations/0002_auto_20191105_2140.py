# Generated by Django 2.2.6 on 2019-11-05 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copyItems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesterm',
            name='value_id_terms',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
