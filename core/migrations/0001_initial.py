# Generated by Django 4.1.1 on 2023-02-19 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CountdownSeconds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sec', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MazorCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(blank=True, max_length=30, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('num_color', models.CharField(blank=True, max_length=40, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=70, null=True)),
                ('notification', models.TextField(max_length=500)),
                ('is_seen', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('desc', models.CharField(blank=True, max_length=70, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimeCapture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_name', models.CharField(blank=True, max_length=50, null=True)),
                ('sub_content_name', models.CharField(blank=True, max_length=50, null=True)),
                ('ref_name', models.CharField(blank=True, max_length=50, null=True)),
                ('iscolor', models.BooleanField(default=False)),
                ('gems', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expired', models.BooleanField(default=False)),
                ('won', models.BooleanField(default=False)),
                ('won_money', models.IntegerField(default=0)),
                ('unique_key', models.CharField(default='null', max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_relation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transtions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transtion_id', models.CharField(blank=True, max_length=30, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('desc', models.CharField(blank=True, max_length=20, null=True)),
                ('money', models.CharField(blank=True, max_length=20, null=True)),
                ('fluctuate_gems', models.FloatField(blank=True, null=True)),
                ('updates_gems', models.FloatField(blank=True, null=True)),
                ('fees', models.IntegerField(default=0)),
                ('refund', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transition_relation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]