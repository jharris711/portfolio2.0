# Generated by Django 3.0.7 on 2020-07-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200702_0538'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image_url_alt',
            field=models.TextField(blank=True, null=True),
        ),
    ]
