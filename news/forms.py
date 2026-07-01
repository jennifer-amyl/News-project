from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Article, CustomUser, Newsletter
from .models import Article, CustomUser, Newsletter, Publisher


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2',
        ]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'publisher',
        ]


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            'title',
            'description',
            'articles',
        ]

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = [
            'name',
            'description',
            'editors',
            'journalists',
        ]