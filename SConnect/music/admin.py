from django.contrib import admin

from .models import User, Track, Invite, Like

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nickname', 'avatar')
    search_fields = ('username', 'nickname')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'like_count')
    list_filter = ('created_at', 'owner', 'collaborators')
    search_fields = ('title', 'owner__username', 'collaborators__username')
    filter_horizontal = ('collaborators',)

    def like_count(self, obj):
        return obj.like_count()
    like_count.short_description = 'Лайков'

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('track_title', 'from_user', 'to_user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('track_title', 'from_user__username', 'to_user__username')
    actions = ['mark_accepted', 'mark_rejected']

    def mark_accepted(self, request, queryset):
        queryset.update(status='accepted')
    mark_accepted.short_description = 'Отметить как принятые'

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = 'Отметить как отклонённые'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'created_at')
    search_fields = ('user__username', 'track__title')
