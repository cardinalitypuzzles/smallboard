# Generated by Django 3.1.4 on 2020-12-28 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("answers", "0004_auto_20201227_0419"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="updated_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
