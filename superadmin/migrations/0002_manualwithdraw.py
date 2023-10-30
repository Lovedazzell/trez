# Generated by Django 4.1.1 on 2023-04-22 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_notification_notification'),
        ('superadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualWithdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_status', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.transtions')),
            ],
        ),
    ]
