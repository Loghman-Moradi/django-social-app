import json

from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from mysocial import settings
from .models import *
from taggit.models import Tag
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def profile(request):
    user = request.user
    saved_posts = user.saved_posts.all()
    return render(request, 'social/profile.html', {'saved_posts': saved_posts})


def log_out(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = EditUserForm(instance=request.user)
    return render(request, 'registration/edit_user.html', {'user_form': user_form})



def ticket(request):
    ticket_create = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user_ticket_id = request.user
            ticket.save()
            ticket_create = True
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form, 'ticket_create': ticket_create})

@login_required
def user_ticket(request):
    tickets = Ticket.objects.filter(user_ticket_id=request.user)
    return render(request, 'social/user_ticket.html', {'tickets': tickets})


def post_list(request, tag_slug=None):
    posts = Post.objects.select_related('author').all().order_by('-total_likes')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])

    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except EmptyPage:
        posts = []
    except PageNotAnInteger:
        posts = paginator.page(1)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'social/list_ajax.html', {'posts': posts})
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, 'social/list.html', context)


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            Image.objects.create(file_image=form.cleaned_data['image_1'], post=post)
            Image.objects.create(file_image=form.cleaned_data['image_2'], post=post)
            return redirect('social:home')
    else:
        form = PostForm()
    return render(request, 'forms/create_post.html', {"form": form})


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=post_tag_ids)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[2:]
    context = {
        'post': post,
        'similar_post': similar_post,
    }
    return render(request, 'social/post_detail.html', context)


def search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(trigram=TrigramSimilarity('description', query)).\
                    filter(trigram__gte=0.1).order_by('-trigram')
        context = {
            'query': query,
            'results': results,
            }
        return render(request, 'forms/search.html', context)


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(
        post=post,
        name=request.user,
        description=request.POST['description'],
    )

    return JsonResponse({
        'name': comment.name.username,
        'description': comment.description,
        'created': comment.created,
    })


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(file_image=form.cleaned_data['image_1'], post=post)
            Image.objects.create(file_image=form.cleaned_data['image_2'], post=post)
            return redirect('social:posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'forms/create_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('social:posts')
    return render(request, 'social/delete_post.html', {'post': post})

def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('social:posts')


@login_required
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        post_likes_count = post.likes.count()
        response_data = {
            'liked': liked,
            'likes_count': post_likes_count,
        }
    else:
        response_data = {'error': 'Invalid post_id'}

    return JsonResponse(response_data)


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = Post.objects.get(id=post_id)
        user = request.user

        if user in post.saves.all():
            post.saves.remove(user)
            saved = False

        else:
            post.saves.add(user)
            saved = True

        response_data = {
            'saved': saved,
        }

        return JsonResponse(response_data)
    return JsonResponse({'error': 'Invalid save id'})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'user/user_list.html', {'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'user/user_detail.html', {'user': user})


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            if request.user in user.followers.all():
                Contact.objects.get(user_from=request.user, user_to=user).delete()
                follow = False

            else:
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                follow = True

            following_count = user.following.count()
            followers_count = user.followers.count()

            return JsonResponse({'follow': follow, 'following_count': following_count,
                                 'followers_count': followers_count})

        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})
    return JsonResponse({'error': 'Invalid user id'})


def user_followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = user.followers.all()
    follower_list = [{'id': follower.id, 'name': follower.get_username()} for follower in followers]
    return JsonResponse({'followers': follower_list})


def user_following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    following = user.following.all()
    following_list = [{'id': followed.id, 'name': followed.get_username()} for followed in following]
    return JsonResponse({'following': following_list})






























