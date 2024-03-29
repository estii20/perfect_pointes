# Generated by Django 3.2.23 on 2024-01-15 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20240115_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Width',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.CharField(choices=[('x', 'X'), ('xx', 'XX'), ('xxx', 'XXX'), ('xxxx', 'XXXX'), ('xxxxx', 'XXXXX')], max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='pointeshoe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='pointeshoe',
            name='image_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.RemoveField(
            model_name='pointeshoe',
            name='available_sizes',
        ),
        migrations.RemoveField(
            model_name='pointeshoe',
            name='available_widths',
        ),
        migrations.AddField(
            model_name='pointeshoe',
            name='available_sizes',
            field=models.ManyToManyField(to='products.Size'),
        ),
        migrations.AddField(
            model_name='pointeshoe',
            name='available_widths',
            field=models.ManyToManyField(to='products.Width'),
        ),
    ]
