# Generated by Django 4.1.1 on 2022-09-06 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=200)),
                ('is_completed', models.BooleanField(default=False)),
                ('priority', models.CharField(choices=[('Very High', 'Very High'), ('High', 'high'), ('Normal', 'normal'), ('Low', 'low'), ('Very Low', 'very low')], default='Normal', max_length=50, verbose_name='Priority')),
            ],
        ),
    ]