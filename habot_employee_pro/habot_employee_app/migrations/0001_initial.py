# Generated by Django 4.2.16 on 2024-11-02 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('department', models.CharField(blank=True, max_length=50, null=True)),
                ('role', models.CharField(blank=True, max_length=50, null=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(max_length=255)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField(null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(max_length=254, null=True)),
                ('is_staff', models.IntegerField(default=1)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.IntegerField(default=1)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(default=None, max_length=10, primary_key=True, serialize=False)),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('user_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('is_verified', models.CharField(default=0, max_length=255)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
                ('user_email', models.CharField(max_length=255, unique=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('user_password', models.CharField(max_length=255)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('first_login', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
