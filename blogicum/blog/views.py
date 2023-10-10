from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import CommentForm, PostForm, UserEditForm
from .mixins import AuthorMixin, CommentMixin, PostMixin, SetMixin
from .models import Category, Comment, Post, User


class IndexListView(SetMixin, generic.ListView):
    template_name = 'blog/index.html'


class PostDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get_object(self):
        self.post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        if ((self.post.is_published is False
                or self.post.category.is_published is False
                or self.post.pub_date > timezone.now())
                and self.post.author != self.request.user):
            raise Http404
        return self.post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = (self.object.comments.select_related('author'))
        return context


class CategoryPostListView(SetMixin, generic.ListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return queryset.filter(
            category=self.category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def get_success_url(self):
        return reverse('blog:profile', args=(self.request.user.username,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostMixin, AuthorMixin,
                     generic.UpdateView):

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.kwargs['post_id'],))


class PostDeleteView(LoginRequiredMixin, PostMixin, AuthorMixin,
                     generic.DeleteView, generic.edit.FormMixin):

    def get_success_url(self):
        return reverse('blog:profile', args=(self.request.user.username,))


class ProfileListView(SetMixin, generic.ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.profile = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        if self.request.user.username != self.kwargs['username']:
            return queryset.filter(
                author__username=self.profile
            )
        return Post.objects.filter(
            author__username=self.profile
        ).annotate(comment_count=models.Count('comments')).order_by(
                '-pub_date'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
        return context


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserEditForm

    def get_object(self):
        user = self.request.user
        return user

    def get_success_url(self):
        return reverse('blog:profile',
                       args=(self.request.user.username,)
                       )


class CommentCreateView (LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       args=(self.kwargs['post_id'],)
                       )


class CommentUpdateView (LoginRequiredMixin, CommentMixin, AuthorMixin,
                         generic.UpdateView):
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail',
                       args=(self.kwargs['post_id'],)
                       )


class CommentDeleteView(LoginRequiredMixin, CommentMixin, AuthorMixin,
                        generic.DeleteView):

    def get_success_url(self):
        return reverse('blog:post_detail',
                       args=(self.kwargs['post_id'],)
                       )
