# Generated by Django 4.2.4 on 2023-10-16 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam_System', '0006_alter_computerscience_broad_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='computerscience',
            name='exam_duration',
            field=models.IntegerField(default=0),
        ),
    ]
