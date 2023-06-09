# Generated by Django 3.2 on 2023-02-20 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('admin', 'Admin'), ('moderator', 'Moderator')], default='user', max_length=9, verbose_name='User role'),
        ),
    ]
