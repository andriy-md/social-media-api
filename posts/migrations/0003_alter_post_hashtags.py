# Generated by Django 4.2.4 on 2023-09-13 19:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_alter_hashtag_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="hashtags",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="posts", to="posts.hashtag"
            ),
        ),
    ]
