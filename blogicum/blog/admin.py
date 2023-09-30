from django.contrib import admin

from .models import Category, Location, Post

admin.site.register(Category)
admin.site.register(Location)


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


admin.site.register(Post, PostAdmin)
