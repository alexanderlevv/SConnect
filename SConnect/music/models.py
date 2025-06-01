from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    nickname = models.CharField(max_length=32, unique=True)
    favorite_tracks = models.ManyToManyField('Track', related_name='favorited_by', blank=True)
    
    def __str__(self):
        return self.nickname or self.username

class Track(models.Model):
    title = models.CharField(max_length=128)
    audio_file = models.FileField(upload_to='tracks/audio/')
    cover_image = models.ImageField(upload_to='tracks/covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_tracks')
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaborations', blank=True)
    
    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

class Invite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invites')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_invites')
    track_title = models.CharField(max_length=128)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} → {self.to_user}: {self.track_title} ({self.status})"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey('Track', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')

    def __str__(self):
        return f"{self.user} likes {self.track}"
