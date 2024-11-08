# Generated by Django 4.2.16 on 2024-11-02 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habot_employee_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HabotAuthtoken',
            fields=[
                ('digest', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('token_key', models.CharField(max_length=8)),
                ('created', models.DateTimeField()),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('digest', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('token_key', models.CharField(db_index=True, max_length=8)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
