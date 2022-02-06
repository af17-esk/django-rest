from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Post
from .serializers import PostSerializer


class PostView(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = Post.objects.filter(user__isnull=True)
            return queryset
        if self.request.method in ['PUT', 'PATCH']:
            queryset = Post.objects.filter(user=self.request.user)
        else:
            queryset = Post.objects.all()
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_anonymous:
            serializer.save(user=self.request.user)
        serializer.save()
