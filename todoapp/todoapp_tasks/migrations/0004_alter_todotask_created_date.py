# Generated by Django 4.1.1 on 2022-09-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp_tasks', '0003_alter_todotask_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todotask',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]