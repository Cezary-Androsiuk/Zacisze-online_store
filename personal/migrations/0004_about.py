# Generated by Django 5.0 on 2023-12-11 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=4000, null=True)),
            ],
        ),
    ]