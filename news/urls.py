from django.urls import path

from . import views

from rest_framework.authtoken.views import obtain_auth_token
from . import api_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/create/', views.create_article, name='create_article'),

    path('approve/', views.approve_articles, name='approve_articles'),
    path('approve/<int:article_id>/', views.approve_article, name='approve_article'),

    path('articles/mine/', views.my_articles, name='my_articles'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:article_id>/delete/', views.delete_article, name='delete_article'),

    path('newsletters/', views.newsletter_list, name='newsletter_list'),
    path('newsletters/create/', views.create_newsletter, name='create_newsletter'),
    path('newsletters/<int:newsletter_id>/', views.newsletter_detail, name='newsletter_detail'),
    path('newsletters/<int:newsletter_id>/edit/', views.edit_newsletter, name='edit_newsletter'),
    path('newsletters/<int:newsletter_id>/delete/', views.delete_newsletter, name='delete_newsletter'),

    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/create/', views.create_publisher, name='create_publisher'),
    path('publishers/<int:publisher_id>/', views.publisher_detail, name='publisher_detail'),

    path('api/token/', obtain_auth_token, name='api_token'),
    path('api/articles/', api_views.ArticleListCreateAPI.as_view(), name='api_articles'),
    path('api/articles/subscribed/', api_views.SubscribedArticlesAPI.as_view(), name='api_subscribed_articles'),
    path('api/articles/<int:pk>/', api_views.ArticleDetailAPI.as_view(), name='api_article_detail'),
    path('api/approved/', api_views.ApprovedArticleLogAPI.as_view(), name='api_approved_log'),

    path('subscriptions/', views.manage_subscriptions, name='manage_subscriptions'),
    path('subscriptions/publisher/<int:publisher_id>/', views.toggle_publisher_subscription, name='toggle_publisher_subscription'),
    path('subscriptions/journalist/<int:journalist_id>/', views.toggle_journalist_subscription, name='toggle_journalist_subscription'),
]