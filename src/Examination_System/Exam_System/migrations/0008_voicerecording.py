# Generated by Django 4.2.4 on 2023-10-17 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam_System', '0007_computerscience_exam_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceRecording',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('audio_file', models.FileField(upload_to='voice_recordings/')),
            ],
        ),
    ]
