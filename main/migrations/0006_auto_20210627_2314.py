# Generated by Django 3.2.4 on 2021-06-27 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210622_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='donation',
            name='categories',
            field=models.ManyToManyField(to='main.Category'),
        ),
    ]
