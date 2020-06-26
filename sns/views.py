from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.utils import timezone

from .forms import UserCreateForm, LoginForm, PostForm, ProfileEditForm

from .models import User, Message


def timeline(request):
    latest_message_list = Message.objects.order_by('-pub_date')
    context = {'latest_message_list': latest_message_list}
    return render(request, 'sns/timeline.html', context)


def userpage(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    latest_message_list = user.message_set.order_by('-pub_date')
    post_user = request.user
    return render(request, 'sns/userpage.html',
                  {'user': user, 'post_user': post_user, 'latest_message_list': latest_message_list})


class ProfileEdit(LoginRequiredMixin, UpdateView):
    def post(self, request, *args, **kwargs):
        user = request.user
        initial_dict = {
            'username': user.username,
            'email': user.email,
            'biography': user.biography,
        }
        form = ProfileEditForm(request.POST or None, request.FILES or None, initial=initial_dict, instance=user)
        if request.method == 'POST':
            if form.is_valid():
                user.username = form.cleaned_data.get('username')
                user.email = form.cleaned_data.get('email')
                user.icon_image = form.cleaned_data.get('icon_image')
                user.biography = form.cleaned_data.get('biography')
                user.save()
                latest_message_list = user.message_set.order_by('-pub_date')
                return render(request, 'sns/userpage.html', {'user': user, 'post_user': user, 'latest_message_list': latest_message_list})
        return render(request, 'sns/edit.html', {'form': form, 'user': user})

    def get(self, request, *args, **kwargs):
        user = request.user
        initial_dict = {
            'username': user.username,
            'email': user.email,
            'biography': user.biography,
        }
        form = ProfileEditForm(request.POST or None, request.FILES or None, initial=initial_dict, instance=user)
        return render(request, 'sns/edit.html', {'form': form, 'user': user})


edit = ProfileEdit.as_view()


def detail(request, user_id, message_id):
    message = get_object_or_404(Message, pk=message_id)
    children_message_list = Message.objects.filter(parent=message_id).order_by('-pub_date')[:5]
    visit_user = request.user
    return render(request, 'sns/detail.html',
                  {'message': message, 'children_message_list': children_message_list, 'visit_user': visit_user})


def delete_confirm(request, user_id, message_id):
    message = get_object_or_404(Message, pk=message_id)
    visit_user = request.user
    return render(request, 'sns/delete_confirm.html', {'message': message, 'visit_user': visit_user})


def delete(request, user_id, message_id):
    message = get_object_or_404(Message, pk=message_id)
    visit_user = request.user
    if message.user.id == visit_user.id:
        message.delete()
    return redirect('/')


def good(request, user_id, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, pk=message_id)
        message.good += 1
        message.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


class PostMessage(CreateView):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('context')
            im = form.cleaned_data.get('image')
            post_user = request.user
            post_user.message_set.create(context=text, image=im, pub_date=timezone.now())
            return redirect('/')
        return render(request, 'sns/post.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        return render(request, 'sns/post.html', {'form': form, })


post = PostMessage.as_view()


class ReplyMessage(CreateView):
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('context')
            im = form.cleaned_data.get('image')
            post_user = request.user
            parent = get_object_or_404(Message, pk=self.kwargs.get('message_id'))
            post_user.message_set.create(context=text, image=im, parent=parent, pub_date=timezone.now())
            return redirect('/')
        message = get_object_or_404(Message, pk=self.kwargs.get('message_id'))
        return render(request, 'sns/reply.html', {'form': form, 'message': message})

    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        message = get_object_or_404(Message, pk=self.kwargs.get('message_id'))
        return render(request, 'sns/reply.html', {'form': form, 'message': message})


reply = ReplyMessage.as_view()


class CreateAccount(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            # フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            # フォームから'email'を読み取る
            email = form.cleaned_data.get('email')
            # フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, email=email, password=password)
            login(request, user)
            return redirect('/')
        return render(request, 'sns/create.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, 'sns/create.html', {'form': form, })


create_account = CreateAccount.as_view()


class AccountLogin(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/')
        return render(request, 'sns/login.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'sns/login.html', {'form': form, })


account_login = AccountLogin.as_view()


class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'sns/timeline.html'





