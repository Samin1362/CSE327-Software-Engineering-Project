# Generated by Django 4.2.4 on 2023-10-29 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam_System', '0003_alter_computerscience_broad_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computerscience',
            name='mcq_question',
            field=models.JSONField(default=list),
        ),
    ]
