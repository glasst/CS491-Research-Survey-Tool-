# Generated by Django 2.0.1 on 2018-02-09 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20180207_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
    ]