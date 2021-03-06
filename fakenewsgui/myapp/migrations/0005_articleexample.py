# Generated by Django 3.1.5 on 2021-02-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20210201_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleExample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_text', models.TextField()),
                ('bias_score', models.FloatField()),
                ('bias_class', models.IntegerField()),
                ('quality_score', models.FloatField()),
                ('quality_class', models.IntegerField()),
                ('origin_url', models.TextField()),
                ('origin_source', models.TextField()),
            ],
        ),
    ]
