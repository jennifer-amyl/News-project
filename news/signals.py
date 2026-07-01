from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article, CustomUser, Newsletter


def create_role_groups():
    reader_group, _ = Group.objects.get_or_create(name='Reader')
    journalist_group, _ = Group.objects.get_or_create(name='Journalist')
    editor_group, _ = Group.objects.get_or_create(name='Editor')

    article_content_type = ContentType.objects.get_for_model(Article)
    newsletter_content_type = ContentType.objects.get_for_model(Newsletter)

    view_article = Permission.objects.get(
        codename='view_article',
        content_type=article_content_type
    )
    add_article = Permission.objects.get(
        codename='add_article',
        content_type=article_content_type
    )
    change_article = Permission.objects.get(
        codename='change_article',
        content_type=article_content_type
    )
    delete_article = Permission.objects.get(
        codename='delete_article',
        content_type=article_content_type
    )

    view_newsletter = Permission.objects.get(
        codename='view_newsletter',
        content_type=newsletter_content_type
    )
    add_newsletter = Permission.objects.get(
        codename='add_newsletter',
        content_type=newsletter_content_type
    )
    change_newsletter = Permission.objects.get(
        codename='change_newsletter',
        content_type=newsletter_content_type
    )
    delete_newsletter = Permission.objects.get(
        codename='delete_newsletter',
        content_type=newsletter_content_type
    )

    reader_group.permissions.set([
        view_article,
        view_newsletter,
    ])

    journalist_group.permissions.set([
        view_article,
        add_article,
        change_article,
        delete_article,
        view_newsletter,
        add_newsletter,
        change_newsletter,
        delete_newsletter,
    ])

    editor_group.permissions.set([
        view_article,
        change_article,
        delete_article,
        view_newsletter,
        change_newsletter,
        delete_newsletter,
    ])


@receiver(post_save, sender=CustomUser)
def assign_user_to_role_group(sender, instance, **kwargs):
    create_role_groups()

    instance.groups.clear()

    if instance.role == CustomUser.READER:
        group = Group.objects.get(name='Reader')
    elif instance.role == CustomUser.JOURNALIST:
        group = Group.objects.get(name='Journalist')
    elif instance.role == CustomUser.EDITOR:
        group = Group.objects.get(name='Editor')
    else:
        return

    instance.groups.add(group)