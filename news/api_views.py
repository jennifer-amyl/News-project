from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer


class ArticleListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Article.objects.filter(approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        if self.request.user.role != 'journalist':
            raise PermissionError('Only journalists can create articles.')

        serializer.save(author=self.request.user, approved=False)


class SubscribedArticlesAPI(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        publisher_ids = user.publisher_subscriptions.values_list('id', flat=True)
        journalist_ids = user.journalist_subscriptions.values_list('id', flat=True)

        return Article.objects.filter(
            approved=True
        ).filter(
            publisher_id__in=publisher_ids
        ) | Article.objects.filter(
            approved=True,
            author_id__in=journalist_ids
        )


class ArticleDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Article.objects.all()

    def perform_update(self, serializer):
        user = self.request.user

        if user.role not in ['journalist', 'editor']:
            raise PermissionError('You cannot update articles.')

        article = self.get_object()

        if user.role == 'journalist' and article.author != user:
            raise PermissionError('You can only update your own articles.')

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role not in ['journalist', 'editor']:
            raise PermissionError('You cannot delete articles.')

        if user.role == 'journalist' and instance.author != user:
            raise PermissionError('You can only delete your own articles.')

        instance.delete()


class ApprovedArticleLogAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        return Response(
            {
                'message': 'Approved article logged successfully.',
                'data': request.data,
            },
            status=status.HTTP_201_CREATED
        )