# Generated by Django 5.0.6 on 2024-06-08 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_catalog',
            field=models.BooleanField(default=True, verbose_name='В каталоге'),
        ),
        migrations.AddField(
            model_name='product',
            name='sketchfab_embed',
            field=models.TextField(blank=True, verbose_name='Код для встраивания Sketchfab'),
        ),
    ]
