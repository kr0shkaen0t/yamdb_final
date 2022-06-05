# Generated by Django 2.2.16 on 2022-03-12 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='titles', to='reviews.Genre', verbose_name='Жанр'),
        ),
    ]