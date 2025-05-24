from django.urls import path
from . import views

urlpatterns = [
    path('active/', views.ActiveChallengesView.as_view(), name='active_challenges'),
    path('user/', views.UserChallengesView.as_view(), name='user_challenges'),
    path('<int:challenge_id>/start/', views.start_challenge, name='start_challenge'),
    path('<int:challenge_id>/progress/', views.update_challenge_progress, name='update_challenge_progress'),
    path('<int:challenge_id>/quiz/', views.get_quiz, name='get_quiz'),
    path('<int:challenge_id>/quiz/submit/', views.submit_quiz, name='submit_quiz'),
]