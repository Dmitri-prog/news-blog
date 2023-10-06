from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from blogicum.settings import LIMIT_MIN

from .forms import CommentForm, PostForm, UserEditForm
from .mixins import AuthorMixin
from .models import Category, Comment, Post, User


class IndexListView(generic.ListView):
    queryset = Post.objects.select_related(
        'category', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(
        comment_count=models.Count('comments')
    ).order_by('-pub_date',)
    template_name = 'blog/index.html'
    paginate_by = LIMIT_MIN


class PostDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get_queryset(self):
        self.post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        if (self.post.is_published is False
                or self.post.category.is_published is False
                or self.post.pub_date > timezone.now()):
            if self.post.author != self.request.user:
                raise Http404
        return Post.objects.filter(id=self.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (self.object.comments.select_related('author'))
        return context


class CategoryPostListView(generic.ListView):

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category=self.category
        ).annotate(
            comment_count=models.Count('comments')
        ).order_by('-pub_date',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    template_name = 'blog/category.html'
    paginate_by = LIMIT_MIN


class PostCreateView(LoginRequiredMixin, generic.CreateView,):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            args=(self.request.user.username,)
                            )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, AuthorMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs['post_id'],)
                            )


class PostDeleteView(LoginRequiredMixin,
                     AuthorMixin, generic.DeleteView, generic.edit.FormMixin):
    form_class = PostForm
    model = Post
    template_name = 'blog/create_post.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            args=(self.request.user.username,)
                            )


class ProfileListView(generic.ListView):
    def get_queryset(self):
        self.profile = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        if self.request.user.username != self.kwargs['username']:
            return Post.objects.filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                author__username=self.profile
            ).annotate(comment_count=models.Count('comments')).order_by(
                '-pub_date',)
        return Post.objects.filter(
            author__username=self.profile).annotate(
            comment_count=models.Count('comments')).order_by('-pub_date',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    template_name = 'blog/profile.html'
    paginate_by = LIMIT_MIN


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserEditForm

    def get_object(self):
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            args=(self.request.user.username,)
                            )


class CommentCreateView (LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    context_object_name = 'comments'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs['post_id'],)
                            )


class CommentUpdateView (LoginRequiredMixin, AuthorMixin, generic.UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs['post_id'],)
                            )


class CommentDeleteView(LoginRequiredMixin, AuthorMixin, generic.DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = get_object_or_404(
            Comment,
            id=self.kwargs['comment_id']
        )
        context['comment'] = comment
        return context

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            args=(self.kwargs['post_id'],)
                            )
