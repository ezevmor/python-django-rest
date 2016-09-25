from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.views import View
from posts.models import Post, VISIBILITY_PUBLIC
from users.forms import LoginForm, SignupForm, BlogForm
from users.models import Profile


class BlogsListView(View):
    def get(self, request):
        """
        renderiza el listado de blogs en el sistema
        :param request:
        :return:
        """
        visible_blogs_list = Profile.objects.filter(visible_blog=True).select_related()
        context = {'blogs_list': visible_blogs_list}
        return render(request, 'users/blog_list.html', context)


class BlogDetailView(View):
    def get(self, request, pk):
        """
        renderiza el blog de un usuario
        :param request:
        :return:
        """
        possible_blogs = User.objects.select_related().filter(pk=pk)
        if len(possible_blogs) != 0:
            if not hasattr(possible_blogs[0], 'profile'):
                return HttpResponseNotFound("El blog que buscas no existe")

        possible_posts = Post.objects.filter(owner_id=pk).order_by('-created_at')

        if len(possible_blogs) == 0:
            return HttpResponseNotFound("El blog que buscas no existe")
        else:
            if request.user.is_authenticated():
                user_posts = possible_posts
            else:
                user_posts = possible_posts.filter(visibility=VISIBILITY_PUBLIC)

        blogfound = possible_blogs[0]

        context = {'blog': blogfound, 'user_posts': user_posts}
        return render(request, 'users/blog_detail.html', context)


class LoginView(View):
    def get(self, request):
        error_message = ""
        login_form = LoginForm()
        context = {'error': error_message, 'form': login_form}
        return render(request, 'users/login.html', context)

    def post(self, request):
        error_message = ""
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('pwd')
            user = authenticate(username=username, password=password)
            if user is None:
                error_message = "Usuario o contraseña incorrectos"
            else:
                if user.is_active:
                    django_login(request, user)
                    return redirect(request.GET.get('next', 'posts_home'))
                else:
                    error_message = "Cuenta de usuario inactiva"

        context = {'error': error_message, 'form': login_form}
        return render(request, 'users/login.html', context)


class LogoutView(View):
    def get(self, request):
        """
        Hace el logout
        :param request:
        :return:
        """
        if request.user.is_authenticated():
            django_logout(request)
        return redirect('posts_home')


class SignupView(View):
    def get(self, request):
        """
        Renderiza la pantalla de registro
        :param request:
        :return:
        """
        message = ""
        signup_form = SignupForm()
        context = {'error': message, 'form': signup_form}
        return render(request, 'users/signup.html', context)

    def post(self, request):
        message = ""
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():

            new_user = signup_form.save(commit=False)
            password = signup_form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()

            signup_form = SignupForm()
            message = "usuario creado"
        context = {'form': signup_form, 'message': message}
        return render(request, 'users/signup.html', context)