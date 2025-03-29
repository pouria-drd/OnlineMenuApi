# Generated by Django 5.1.7 on 2025-03-29 13:30

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(help_text='Enter a valid email address.', max_length=254, unique=True, validators=[django.core.validators.EmailValidator(code='invalid_email', message='Enter a valid email address.')])),
                ('username', models.CharField(help_text='Required. 25 characters or fewer. Letters, digits, and _ only.', max_length=25, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Username can only contain lowercase letters, numbers, and underscores and must be at most 25 characters long.', regex='^[a-z0-9_]{1,25}$')])),
                ('phone_number', models.CharField(blank=True, help_text='Enter a valid Iranian phone number (e.g., +989123456789 or 09123456789).', max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='Enter a valid Iranian phone number (e.g., +989123456789 or 09123456789).', regex='^(?:\\+98|0)?9\\d{9}$')])),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('-created_at',),
            },
        ),
    ]
