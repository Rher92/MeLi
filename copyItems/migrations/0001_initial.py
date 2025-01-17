# Generated by Django 2.2.6 on 2019-11-05 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('user_id', models.CharField(max_length=40)),
                ('access_token', models.CharField(max_length=100)),
                ('app_id', models.CharField(max_length=100)),
                ('app_secret_key', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meli_id', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('category_id', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=20)),
                ('currency_id', models.CharField(max_length=10)),
                ('available_quantity', models.CharField(max_length=10)),
                ('buying_mode', models.CharField(max_length=30)),
                ('listing_type_id', models.CharField(max_length=30)),
                ('video_id', models.CharField(max_length=100, null=True)),
                ('copy_item', models.CharField(max_length=100, null=True)),
                ('copy', models.BooleanField(default=False)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copyItems.Account')),
            ],
        ),
        migrations.CreateModel(
            name='SalesTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_sale_terms', models.CharField(max_length=30)),
                ('sale_terms', models.CharField(max_length=30)),
                ('value_id_terms', models.CharField(max_length=30)),
                ('publication_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copyItems.PublicationData')),
            ],
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('publication_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copyItems.PublicationData')),
            ],
        ),
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('publication_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copyItems.PublicationData')),
            ],
        ),
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_attributes', models.CharField(max_length=30)),
                ('value_attributes', models.CharField(max_length=30)),
                ('publication_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='copyItems.PublicationData')),
            ],
        ),
    ]
