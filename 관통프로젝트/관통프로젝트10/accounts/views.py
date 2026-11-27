from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
)

from .forms import CustomUserCreationForm, CustomUserChangeForm


@require_http_methods(["GET", "POST"])
def login(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('books:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('books:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('books:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            selected_categories = form.cleaned_data.get('interested_genres')
            if selected_categories:
                user.interested_genres.set(selected_categories)
            auth_login(request, user)
            return redirect('books:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    context = {
        'person': person,
        'is_following': request.user.is_authenticated and person.followers.filter(pk=request.user.pk).exists(),
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '로그인해 주세요.'}, status=403)
    person = get_object_or_404(get_user_model(), pk=user_pk)
    if person == request.user:
        return JsonResponse({'error': '자기 자신을 팔로우할 수 없습니다.'}, status=400)

    is_following = request.POST.get('active') == 'true'
    if is_following:
        request.user.followings.add(person)
    else:
        request.user.followings.remove(person)
    return JsonResponse({
        'active': is_following,
        'followers': person.followers.count(),
        'followings': person.followings.count(),
    })
