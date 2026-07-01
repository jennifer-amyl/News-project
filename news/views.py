from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .forms import ArticleForm, NewsletterForm
from .models import Article, Newsletter
from .forms import ArticleForm, NewsletterForm, PublisherForm
from .models import Article, Newsletter, Publisher
from .models import Article, CustomUser, Newsletter, Publisher

import requests

from django.conf import settings
from django.core.mail import send_mail

def home(request):
    return render(request, 'news/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'news/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'news/dashboard.html')

def article_list(request):
    articles = Article.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'news/article_list.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, approved=True)
    return render(request, 'news/article_detail.html', {'article': article})


@login_required
def create_article(request):
    if request.user.role != 'journalist':
        messages.error(request, 'Only journalists can create articles.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.approved = False
            article.save()
            messages.success(request, 'Article submitted for approval.')
            return redirect('dashboard')
    else:
        form = ArticleForm()

    return render(request, 'news/create_article.html', {'form': form})

def notify_subscribers(article, request):
    subscribers = set()

    journalist_subscribers = CustomUser.objects.filter(
        journalist_subscriptions=article.author
    )
    subscribers.update(journalist_subscribers)

    if article.publisher:
        publisher_subscribers = CustomUser.objects.filter(
            publisher_subscriptions=article.publisher
        )
        subscribers.update(publisher_subscribers)

    for subscriber in subscribers:
        if subscriber.email:
            send_mail(
                subject=f'New approved article: {article.title}',
                message=article.content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=False,
            )

    api_url = request.build_absolute_uri('/api/approved/')

    requests.post(
        api_url,
        json={
            'id': article.id,
            'title': article.title,
            'author': article.author.username,
            'publisher': article.publisher.name if article.publisher else None,
        },
        timeout=5,
    )

@login_required
def approve_articles(request):

    if request.user.role != 'editor':
        messages.error(request, 'Only editors can approve articles.')
        return redirect('dashboard')

    articles = Article.objects.filter(approved=False)

    return render(
        request,
        'news/approve_articles.html',
        {'articles': articles}
    )


@login_required
def approve_article(request, article_id):

    if request.user.role != 'editor':
        messages.error(request, 'Only editors can approve articles.')
        return redirect('dashboard')

    article = get_object_or_404(Article, id=article_id)

    article.approved = True
    article.save()

    notify_subscribers(article, request)

    messages.success(request, 'Article approved and subscribers notified.')

    return redirect('approve_articles')

@login_required
def my_articles(request):
    if request.user.role != 'journalist':
        messages.error(request, 'Only journalists can view their articles.')
        return redirect('dashboard')

    articles = Article.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'news/my_articles.html', {'articles': articles})


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user.role == 'journalist' and article.author != request.user:
        messages.error(request, 'You can only edit your own articles.')
        return redirect('dashboard')

    if request.user.role not in ['journalist', 'editor']:
        messages.error(request, 'You do not have permission to edit articles.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            edited_article = form.save(commit=False)

            if request.user.role == 'journalist':
                edited_article.approved = False

            edited_article.save()
            messages.success(request, 'Article updated.')
            return redirect('my_articles' if request.user.role == 'journalist' else 'approve_articles')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'news/edit_article.html', {'form': form})


@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user.role == 'journalist' and article.author != request.user:
        messages.error(request, 'You can only delete your own articles.')
        return redirect('dashboard')

    if request.user.role not in ['journalist', 'editor']:
        messages.error(request, 'You do not have permission to delete articles.')
        return redirect('dashboard')

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted.')
        return redirect('dashboard')

    return render(request, 'news/delete_article.html', {'article': article})

def newsletter_list(request):
    newsletters = Newsletter.objects.all().order_by('-created_at')
    return render(request, 'news/newsletter_list.html', {'newsletters': newsletters})


def newsletter_detail(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    return render(request, 'news/newsletter_detail.html', {'newsletter': newsletter})


@login_required
def create_newsletter(request):
    if request.user.role not in ['journalist', 'editor']:
        messages.error(request, 'Only journalists and editors can create newsletters.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = NewsletterForm(request.POST)

        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()
            messages.success(request, 'Newsletter created.')
            return redirect('newsletter_list')
    else:
        form = NewsletterForm()

    return render(request, 'news/create_newsletter.html', {'form': form})


@login_required
def edit_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.user.role == 'journalist' and newsletter.author != request.user:
        messages.error(request, 'You can only edit your own newsletters.')
        return redirect('dashboard')

    if request.user.role not in ['journalist', 'editor']:
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = NewsletterForm(request.POST, instance=newsletter)

        if form.is_valid():
            form.save()
            messages.success(request, 'Newsletter updated.')
            return redirect('newsletter_detail', newsletter_id=newsletter.id)
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, 'news/edit_newsletter.html', {'form': form})


@login_required
def delete_newsletter(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.user.role == 'journalist' and newsletter.author != request.user:
        messages.error(request, 'You can only delete your own newsletters.')
        return redirect('dashboard')

    if request.user.role not in ['journalist', 'editor']:
        messages.error(request, 'You do not have permission.')
        return redirect('dashboard')

    if request.method == 'POST':
        newsletter.delete()
        messages.success(request, 'Newsletter deleted.')
        return redirect('newsletter_list')

    return render(request, 'news/delete_newsletter.html', {'newsletter': newsletter})

def publisher_list(request):
    publishers = Publisher.objects.all().order_by('name')
    return render(request, 'news/publisher_list.html', {'publishers': publishers})


def publisher_detail(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)
    articles = Article.objects.filter(publisher=publisher, approved=True)

    return render(
        request,
        'news/publisher_detail.html',
        {
            'publisher': publisher,
            'articles': articles,
        }
    )


@login_required
def create_publisher(request):
    if request.user.role != 'editor':
        messages.error(request, 'Only editors can create publishers.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = PublisherForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Publisher created.')
            return redirect('publisher_list')
    else:
        form = PublisherForm()

    return render(request, 'news/create_publisher.html', {'form': form})

@login_required
def manage_subscriptions(request):
    if request.user.role != 'reader':
        messages.error(request, 'Only readers can manage subscriptions.')
        return redirect('dashboard')

    publishers = Publisher.objects.all().order_by('name')
    journalists = CustomUser.objects.filter(role='journalist').order_by('username')

    return render(
        request,
        'news/manage_subscriptions.html',
        {
            'publishers': publishers,
            'journalists': journalists,
        }
    )


@login_required
def toggle_publisher_subscription(request, publisher_id):
    if request.user.role != 'reader':
        messages.error(request, 'Only readers can subscribe to publishers.')
        return redirect('dashboard')

    publisher = get_object_or_404(Publisher, id=publisher_id)

    if publisher in request.user.publisher_subscriptions.all():
        request.user.publisher_subscriptions.remove(publisher)
        messages.success(request, f'Unsubscribed from {publisher.name}.')
    else:
        request.user.publisher_subscriptions.add(publisher)
        messages.success(request, f'Subscribed to {publisher.name}.')

    return redirect('manage_subscriptions')


@login_required
def toggle_journalist_subscription(request, journalist_id):
    if request.user.role != 'reader':
        messages.error(request, 'Only readers can subscribe to journalists.')
        return redirect('dashboard')

    journalist = get_object_or_404(CustomUser, id=journalist_id, role='journalist')

    if journalist in request.user.journalist_subscriptions.all():
        request.user.journalist_subscriptions.remove(journalist)
        messages.success(request, f'Unsubscribed from {journalist.username}.')
    else:
        request.user.journalist_subscriptions.add(journalist)
        messages.success(request, f'Subscribed to {journalist.username}.')

    return redirect('manage_subscriptions')

from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import ArticleForm
from .models import Article