# Generated by Django 3.2.23 on 2024-01-17 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20240117_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointeshoeproduct',
            name='image_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
