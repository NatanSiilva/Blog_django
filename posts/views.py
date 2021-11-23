from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from .models import Post
from django.db.models import Q, Count, Case, When
from comments.forms import FormComment
from comments.models import Comment
from django.contrib import messages
from django.views import View
# from django.db import connection


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 4
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('category_post')
        qs = qs.order_by('-id').filter(published_post=True)
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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['connection'] = connection
    #     return context


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

class PostDetails(View):
    template_name = 'posts/post_details.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk, published_post=True)
        comments = Comment.objects.filter(post_comment=post, publish_comment=True)
        form = FormComment(request.POST or None)

        self.context = {
            'post': post,
            'comments': comments,
            'form': form
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.context['form']

        if not form.is_valid():
            return render(request, self.template_name, self.context)
        
        comment = form.save(commit=False)  

        if self.request.user.is_authenticated:
            comment.user_comment = self.request.user

        comment.post_comment = self.context['post']
        comment.save()

        messages.success(self.request, 'Comentário enviado com sucesso!')
        return redirect('post_details', pk=self.kwargs.get('pk'))




# class PostDetails(UpdateView):
#     template_name = 'posts/post_details.html'
#     model = Post
#     form_class = FormComment
#     context_object_name = 'post'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = self.get_object()
#         comments = Comment.objects.filter(
#             publish_comment=True, post_comment=post.id)
#         context['comments'] = comments

#         return context

#     def form_valid(self, form):
#         post = self.get_object()
#         comment = Comment(**form.cleaned_data)
#         comment.post_comment = post

#         if self.request.user.is_authenticated:
#             comment.user_comment = self.request.user

#         comment.save()

#         messages.success(self.request, 'Comentário enviado com sucesso!')
#         return redirect('post_details', pk=post.id)
