# Generated by Django 4.0.3 on 2022-03-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_mates', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='googleId',
            new_name='google_id',
        ),
        migrations.AlterField(
            model_name='artist',
            name='description',
            field=models.CharField(max_length=1200),
        ),
    ]
