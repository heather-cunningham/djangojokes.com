# Generated by Django 5.2 on 2025-04-17 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jokes', '0006_tag_joke_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['tag']},
        ),
        migrations.AlterField(
            model_name='joke',
            name='tags',
            field=models.ManyToManyField(blank=True, to='jokes.tag'),
        ),
    ]
