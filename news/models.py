from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    READER = 'reader'
    JOURNALIST = 'journalist'
    EDITOR = 'editor'

    ROLE_CHOICES = [
        (READER, 'Reader'),
        (JOURNALIST, 'Journalist'),
        (EDITOR, 'Editor'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=READER
    )

    publisher_subscriptions = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='subscribers'
    )

    journalist_subscriptions = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='followers'
    )

    def __str__(self):
        return self.username


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    editors = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='editor_publishers'
    )

    journalists = models.ManyToManyField(
        CustomUser,
        blank=True,
        related_name='journalist_publishers'
    )

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='newsletters'
    )

    articles = models.ManyToManyField(
        Article,
        blank=True,
        related_name='newsletters'
    )

    def __str__(self):
        return self.title