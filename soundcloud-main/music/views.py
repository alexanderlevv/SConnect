from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .models import User, Track, Invite, Like
from .forms import RegisterForm, LoginForm, TrackUploadForm
from django.db.models import Count

# Главная страница: популярные и новые треки
def index(request):
    popular_tracks = Track.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:10]
    new_tracks = Track.objects.order_by('-created_at')[:10]
    return render(request, 'music/index.html', {
        'popular_tracks': popular_tracks,
        'new_tracks': new_tracks,
    })

# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'music/register.html', {'form': form})

# Вход
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'music/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

# Профиль пользователя
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    uploaded_tracks = user.owned_tracks.all()
    favorite_tracks = user.favorite_tracks.all()
    collab_tracks = user.collaborations.all()
    return render(request, 'music/profile.html', {
        'profile_user': user,
        'uploaded_tracks': uploaded_tracks,
        'favorite_tracks': favorite_tracks,
        'collab_tracks': collab_tracks,
    })

# Детали трека
def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    is_liked = False
    is_favorited = False
    context = {'track': track, 'is_liked': is_liked, 'is_favorited': is_favorited}
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, track=track).exists()
        is_favorited = track in request.user.favorite_tracks.all()
        context['is_liked'] = is_liked
        context['is_favorited'] = is_favorited
    if 'invite_error' in request.GET:
        context['invite_error'] = request.GET['invite_error']
    if 'invite_success' in request.GET:
        context['invite_success'] = request.GET['invite_success']
    return render(request, 'music/track_detail.html', context)

from django.views.decorators.http import require_POST

@login_required
@require_POST
def send_invite(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    to_user_nick = request.POST.get('to_user', '').strip()
    message = request.POST.get('message', '').strip()
    if not to_user_nick:
        return redirect(f'/track/{track_id}/?invite_error=Укажите+ник+пользователя')
    try:
        to_user = User.objects.get(nickname=to_user_nick)
    except User.DoesNotExist:
        return redirect(f'/track/{track_id}/?invite_error=Пользователь+не+найден')
    if to_user == request.user:
        return redirect(f'/track/{track_id}/?invite_error=Нельзя+пригласить+самого+себя')
    # Проверка на дубликат (pending)
    if Invite.objects.filter(from_user=request.user, to_user=to_user, track_title=track.title, status='pending').exists():
        return redirect(f'/track/{track_id}/?invite_error=У+вас+уже+есть+отправленный+инвайт+этому+пользователю+на+этот+трек')
    Invite.objects.create(
        from_user=request.user,
        to_user=to_user,
        track_title=track.title,
        message=message
    )
    return redirect(f'/track/{track_id}/?invite_success=Инвайт+отправлен')

# Загрузка трека
@login_required
def upload_track(request):
    if request.method == 'POST':
        form = TrackUploadForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.owner = request.user
            track.save()
            form.save_m2m()
            return redirect('profile', username=request.user.username)
    else:
        form = TrackUploadForm()
    return render(request, 'music/upload_track.html', {'form': form})

# Инвайты
@login_required
def invites(request):
    incoming = request.user.received_invites.all()
    outgoing = request.user.sent_invites.all()
    return render(request, 'music/invites.html', {
        'incoming': incoming,
        'outgoing': outgoing,
    })

@login_required
def invite_respond(request, invite_id):
    invite = get_object_or_404(Invite, id=invite_id, to_user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            invite.status = 'accepted'
            invite.save()
            # Создать совместный трек
            track = Track.objects.create(
                title=invite.track_title,
                owner=invite.from_user
            )
            track.collaborators.add(invite.to_user)
        elif action == 'reject':
            invite.status = 'rejected'
            invite.save()
        return redirect('invites')
    return render(request, 'music/invite_respond.html', {'invite': invite})

@login_required
def like_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    liked = Like.objects.filter(user=request.user, track=track)
    if liked.exists():
        liked.delete()
        liked_status = False
    else:
        Like.objects.create(user=request.user, track=track)
        liked_status = True
    return JsonResponse({'liked': liked_status, 'like_count': track.like_count()})

@login_required
def favorite_track(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    if track in request.user.favorite_tracks.all():
        request.user.favorite_tracks.remove(track)
        favorited = False
    else:
        request.user.favorite_tracks.add(track)
        favorited = True
    return JsonResponse({'favorited': favorited})
