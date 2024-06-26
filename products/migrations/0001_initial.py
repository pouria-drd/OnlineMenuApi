# Generated by Django 5.0.4 on 2024-06-14 17:50

import django.db.models.deletion
import products.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='name')),
                ('icon', models.ImageField(blank=True, upload_to=products.models.product_icon_upload_to, verbose_name='icon')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='products', to='categories.category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['name'], name='products_pr_name_9ff0a3_idx')],
            },
        ),
    ]
