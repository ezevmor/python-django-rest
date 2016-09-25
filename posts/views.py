from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views import View
from posts.forms import PostForm
from posts.models import Post, VISIBILITY_PUBLIC


class HomeView(View):
    def get(self, request):
        """
        Renderiza el listado de posts
        :param request:
        :return:
        """
        possible_posts = posts = Post.objects.all()
        if request.user.is_authenticated():
            posts = possible_posts.filter(Q(visibility=VISIBILITY_PUBLIC) | Q(owner=request.user)).order_by('-created_at')
        else:
            posts = possible_posts.filter(visibility=VISIBILITY_PUBLIC).order_by('-created_at')

        context = {'post_list': posts}
        return render(request, "posts/home.html", context)


class PostView(View):
    def get(self, request, pk, id):
        """
        Renderiza el detalle de un post
        :param request:
        :param pk:
        :param id:
        :return:
        """
        possible_posts = Post.objects.filter(owner_id=pk, pk=id)

        if request.user.is_authenticated():
            if len(possible_posts) == 0:
                return HttpResponseNotFound("El post que buscas no existe")
            post = possible_posts[0]
        else:
            publics_posts = possible_posts.filter(visibility=VISIBILITY_PUBLIC)
            if len(publics_posts) == 0:
                return HttpResponseNotFound("El post que buscas no existe")
            post = publics_posts[0]

        context = {'post_detail': post}
        return render(request, "posts/post.html", context)


class CreatePostView(LoginRequiredMixin,View):
    def get(self, request):
        message = None
        post_form = PostForm()
        context = {'form': post_form, 'message': message}
        return render(request, 'posts/create_post.html', context)

    def post(self, request):
        message = None
        post_with_user = Post(owner=request.user)
        post_form = PostForm(request.POST, instance=post_with_user)
        if post_form.is_valid():
            new_post = post_form.save()
            post_form = PostForm()
            message = "Post creado"
        context = {'form': post_form, 'message': message}
        return render(request, 'posts/create_post.html', context)
