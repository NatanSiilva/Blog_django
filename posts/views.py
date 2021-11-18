from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comments.forms import FormComment


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        # qs = qs.order_by('-id').filter(published_post=True)
        qs = qs.order_by('-id')
        qs = qs.annotate(
            num_comments=Count(
                Case(
                    When(
                        comment__publish_comment=True, then=1
                    )
                )
            )
        )

        return qs


class PostSearch(PostIndex):
    template_name = 'posts/post_search.html'

    def get_queryset(self):
        qs = super().get_queryset()

        serach = self.request.GET.get('search')

        if not serach:
            return qs

        qs = qs.filter(
            Q(title_post__icontains=serach) |
            Q(author_post__first_name__iexact=serach) |
            Q(content_post__icontains=serach) |
            Q(excerpt_post__icontains=serach) |
            Q(category_post__name_cat__iexact=serach)
        )

        return qs


class PostCategories(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.kwargs.get('category', None)

        if not category:
            return qs

        qs = qs.filter(category_post__name_cat__iexact=category)

        return qs


class PostDetails(UpdateView):
    template_name = 'posts/post_details.html'
    model = Post
    form_class = FormComment
    context_object_name = 'post'
