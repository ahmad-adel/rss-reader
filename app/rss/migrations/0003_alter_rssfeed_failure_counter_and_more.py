# Generated by Django 4.2.7 on 2023-11-17 22:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("rss", "0002_rename_last_update_rssfeed_last_fetch_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rssfeed",
            name="failure_counter",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="rssfeed",
            name="next_fetch",
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name="rssfeed",
            name="title",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="rsspost",
            name="updated",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddConstraint(
            model_name="rsspost",
            constraint=models.UniqueConstraint(
                fields=("feed", "guid"), name="feed_guid_unique"
            ),
        ),
    ]
