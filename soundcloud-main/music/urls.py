from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('track/<int:track_id>/', views.track_detail, name='track_detail'),
    path('upload/', views.upload_track, name='upload_track'),
    path('invites/', views.invites, name='invites'),
    path('invite/respond/<int:invite_id>/', views.invite_respond, name='invite_respond'),
    path('invite/send/<int:track_id>/', views.send_invite, name='send_invite'),
    path('like/<int:track_id>/', views.like_track, name='like_track'),
    path('favorite/<int:track_id>/', views.favorite_track, name='favorite_track'),
]
