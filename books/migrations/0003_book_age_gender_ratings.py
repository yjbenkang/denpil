# Generated by Django 5.1.2 on 2024-10-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_author_description_author_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="age_gender_ratings",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
