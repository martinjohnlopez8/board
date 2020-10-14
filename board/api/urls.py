from django.urls import path

from . import views

app_label = 'api'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('follow/', views.FollowUserView.as_view()),
    path('unfollow/', views.UnfollowUserView.as_view()),
    path('profile/', views.UserProfileDisplayView.as_view()),
    path('profile/update/', views.UserProfileUpdateView.as_view()),
    path('ban/', views.BanUserView.as_view()),
    path('unban/', views.UnbanUserView.as_view()),
    path('lock-unlock/thread/', views.LockUnlockThread.as_view()),
    path('create/board/', views.BoardCreateView.as_view()),
    path('create/thread/', views.ThreadCreateView.as_view()),
    path('create/post/', views.PostCreateView.as_view()),
    path('boards/', views.BoardListView.as_view()),
    path('post/<int:user_id>', views.UserPostListView.as_view()),
    path('get/gravatar/', views.UserGravatarView.as_view())
]