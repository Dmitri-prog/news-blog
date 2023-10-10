from django.conf import settings
from django.db import models
from django.shortcuts import redirect
from django.utils import timezone

from .forms import PostForm
from .models import Comment, Post


class SetMixin:
    model = Post
    paginate_by = settings.LIMIT_MIN

    def get_queryset(self):
        return Post.objects.select_related(
            'category', 'author', 'location'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(
            comment_count=models.Count('comments')
        ).order_by('-pub_date')


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    pk_url_kwarg = 'post_id'


class AuthorMixin:

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'
