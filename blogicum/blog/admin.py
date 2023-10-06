from django.contrib import admin

from .models import Category, Comment, Location, Post


class CommentInline(admin.TabularInline):
    model = Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
    )
    list_filter = (
        'title',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'post',
        'text',
        'author',
        'created_at'
    )
    list_filter = (
        'author',
        'post'
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_at'
    )
    list_filter = (
        'name',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'pub_date',
        'author',
        'category',
        'location',
        'is_published',
        'created_at',
        'image'
    )
    list_editable = (
        'pub_date',
        'category',
        'location',
        'is_published'
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'category',
    )
    inlines = [
        CommentInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Location, LocationAdmin)
