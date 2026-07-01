from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Article, CustomUser, Newsletter, Publisher


class NewsAppTests(TestCase):

    def setUp(self):
        self.reader = CustomUser.objects.create_user(
            username='reader',
            email='reader@test.com',
            password='testpass123',
            role='reader'
        )

        self.journalist = CustomUser.objects.create_user(
            username='journalist',
            email='journalist@test.com',
            password='testpass123',
            role='journalist'
        )

        self.editor = CustomUser.objects.create_user(
            username='editor',
            email='editor@test.com',
            password='testpass123',
            role='editor'
        )

        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            description='A test publisher'
        )

        self.article = Article.objects.create(
            title='Approved Article',
            content='Approved content',
            author=self.journalist,
            publisher=self.publisher,
            approved=True
        )

        self.pending_article = Article.objects.create(
            title='Pending Article',
            content='Pending content',
            author=self.journalist,
            approved=False
        )

        self.client = APIClient()

    def test_reader_can_view_approved_articles(self):
        self.client.login(username='reader', password='testpass123')
        response = self.client.get(reverse('article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Article')
        self.assertNotContains(response, 'Pending Article')

    def test_journalist_can_create_article(self):
        self.client.login(username='journalist', password='testpass123')

        response = self.client.post(reverse('create_article'), {
            'title': 'New Article',
            'content': 'New content',
            'publisher': self.publisher.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(title='New Article').exists())

    def test_reader_cannot_create_article(self):
        self.client.login(username='reader', password='testpass123')

        response = self.client.post(reverse('create_article'), {
            'title': 'Bad Article',
            'content': 'Should not work',
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(title='Bad Article').exists())

    @patch('news.views.requests.post')
    @patch('news.views.send_mail')
    def test_editor_can_approve_article(self, mock_send_mail, mock_post):
        self.client.login(username='editor', password='testpass123')

        response = self.client.get(
            reverse('approve_article', args=[self.pending_article.id])
        )

        self.pending_article.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.pending_article.approved)
        mock_post.assert_called_once()

    def test_api_returns_only_approved_articles(self):
        self.client.force_authenticate(user=self.reader)

        response = self.client.get(reverse('api_articles'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Article')
        self.assertNotContains(response, 'Pending Article')

    def test_subscribed_articles_api(self):
        self.reader.publisher_subscriptions.add(self.publisher)
        self.client.force_authenticate(user=self.reader)

        response = self.client.get(reverse('api_subscribed_articles'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Article')

    def test_journalist_can_create_newsletter(self):
        self.client.login(username='journalist', password='testpass123')

        response = self.client.post(reverse('create_newsletter'), {
            'title': 'Weekly News',
            'description': 'Newsletter description',
            'articles': [self.article.id],
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newsletter.objects.filter(title='Weekly News').exists())

    def test_reader_cannot_create_newsletter(self):
        self.client.login(username='reader', password='testpass123')

        response = self.client.post(reverse('create_newsletter'), {
            'title': 'Bad Newsletter',
            'description': 'Should not work',
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Newsletter.objects.filter(title='Bad Newsletter').exists()
        )

    def test_editor_can_delete_article(self):
        self.client.login(username='editor', password='testpass123')

        response = self.client.post(
            reverse('delete_article', args=[self.article.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Article.objects.filter(id=self.article.id).exists()
        )

    def test_reader_cannot_delete_article(self):
        self.client.login(username='reader', password='testpass123')

        response = self.client.post(
            reverse('delete_article', args=[self.article.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Article.objects.filter(id=self.article.id).exists()
        )

    def test_reader_can_subscribe_to_publisher(self):
        self.client.login(username='reader', password='testpass123')

        response = self.client.get(
            reverse('toggle_publisher_subscription', args=[self.publisher.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.publisher, self.reader.publisher_subscriptions.all())

    def test_reader_can_subscribe_to_journalist(self):
        self.client.login(username='reader', password='testpass123')

        response = self.client.get(
            reverse('toggle_journalist_subscription', args=[self.journalist.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.journalist, self.reader.journalist_subscriptions.all())

    def test_editor_can_create_publisher(self):
        self.client.login(username='editor', password='testpass123')

        response = self.client.post(reverse('create_publisher'), {
            'name': 'New Publisher',
            'description': 'Created by editor',
            'editors': [self.editor.id],
            'journalists': [self.journalist.id],
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Publisher.objects.filter(name='New Publisher').exists()
        )

    def test_reader_cannot_create_publisher(self):
        self.client.login(username='reader', password='testpass123')

        response = self.client.post(reverse('create_publisher'), {
            'name': 'Bad Publisher',
            'description': 'Should not work',
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Publisher.objects.filter(name='Bad Publisher').exists()
        )