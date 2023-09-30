from blog.forms import CommentForm, PostForm, UserEditForm
from blog.models import Category, Comment, Post, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from blogicum.settings import LIMIT_MIN


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


class PostDetailView(generic.DetailView):
    def get_object(self):
        return get_object_or_404(
            Post,
            id=self.kwargs['pk'],
        )

    def dispatch(self, request, *args, **kwargs):
        if (self.get_object().is_published is False
                or self.get_object().category.is_published is False
                or self.get_object().pub_date > timezone.now()):
            if self.get_object().author != self.request.user:
                raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comments.select_related('author'))
        return context
    template_name = 'blog/detail.html'


class CategoryPostListView(generic.ListView):

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__slug=self.kwargs['category_slug']
        ).annotate(
            comment_count=models.Count('comments')
        ).order_by('-pub_date',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        context['category'] = category
        return context

    template_name = 'blog/category.html'
    paginate_by = LIMIT_MIN


class PostCreateView(LoginRequiredMixin, generic.CreateView,):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username}
                            )

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'

    def get_object(self):
        return get_object_or_404(
            Post,
            id=self.kwargs['post_id'],
        )

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['post_id']})


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'blog/create_post.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PostForm(
            self.request.POST or None,
            instance=context['post']
        )
        context['form'] = form
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username}
                            )


class ProfileListView(generic.ListView):
    def get_queryset(self):
        if self.request.user.username != self.kwargs['username']:
            return Post.objects.filter(
                pub_date__lte=timezone.now(),
                is_published=True,
                author__username=self.kwargs['username']
            ).annotate(
             comment_count=models.Count('comments')
            ).order_by('-pub_date',)
        return Post.objects.filter(
                author__username=self.kwargs['username']
            ).annotate(
             comment_count=models.Count('comments')
            ).order_by('-pub_date',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        context['profile'] = profile
        return context

    template_name = 'blog/profile.html'
    paginate_by = LIMIT_MIN


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'blog/user.html'
    form_class = UserEditForm

    def get_object(self):
        return get_object_or_404(
            User,
            username=self.request.user.username,
        )

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            kwargs={'username': self.request.user.username}
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
                            kwargs={'pk': self.kwargs['post_id']})


class CommentUpdateView (LoginRequiredMixin, generic.UpdateView):
    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_object(self):
        return get_object_or_404(
            Comment,
            id=self.kwargs['comment_id']
        )

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['post_id']}
                            )


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView,):
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

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['post_id']}
                            )
