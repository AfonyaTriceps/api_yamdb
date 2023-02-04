# Generated by Django 3.2 on 2023-02-04 23:20

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=256, verbose_name='Название'),
                ),
                (
                    'slug',
                    models.SlugField(
                        unique=True, verbose_name='Идентификатор'
                    ),
                ),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                (
                    'pub_date',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('pub_date',),
                'default_related_name': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(max_length=256, verbose_name='Название'),
                ),
                (
                    'slug',
                    models.SlugField(
                        unique=True, verbose_name='Идентификатор'
                    ),
                ),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'жанры',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                (
                    'score',
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ],
                        verbose_name='Оценка',
                    ),
                ),
                (
                    'pub_date',
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('pub_date',),
                'default_related_name': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=256, verbose_name='Название произведения'
                    ),
                ),
                (
                    'year',
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(2023)
                        ],
                        verbose_name='Год',
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True, null=True, verbose_name='Описание'
                    ),
                ),
                (
                    'rating',
                    models.IntegerField(
                        default=None, null=True, verbose_name='Рейтинг'
                    ),
                ),
                (
                    'category',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='titles',
                        to='reviews.category',
                        verbose_name='Категория произведения',
                    ),
                ),
            ],
            options={
                'verbose_name': 'произведение',
                'verbose_name_plural': 'произведения',
                'ordering': ('-year',),
                'default_related_name': 'titles',
            },
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'genre',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='reviews.genre',
                        verbose_name='Жанр произведения',
                    ),
                ),
                (
                    'title',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='reviews.title',
                        verbose_name='Произведение',
                    ),
                ),
            ],
            options={
                'verbose_name': 'произведение с жанром',
                'verbose_name_plural': 'произведения с жанрами',
            },
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(
                related_name='titles',
                through='reviews.TitleGenre',
                to='reviews.Genre',
                verbose_name='Жанр',
            ),
        ),
    ]
