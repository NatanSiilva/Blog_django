from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title_post', 'author_post',
                    'date_post', 'published_post', 'category_post')
    list_editable = ('published_post',)
    list_display_links = ('id', 'title_post',)
    sumernote_fields = ('content_post',)
    # list_filter = ('status', 'created', 'publish', 'author')
    # search_fields = ('title', 'body')
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    # date_hierarchy = 'publish'
    # ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)
