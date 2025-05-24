from django.contrib import admin
from .models import Challenge, UserChallenge, Quiz, QuizQuestion, QuizAttempt

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'challenge_type', 'difficulty', 'points_reward', 'is_active']
    list_filter = ['challenge_type', 'difficulty', 'is_active', 'created_at']
    search_fields = ['title', 'description']

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'status', 'progress', 'started_at']
    list_filter = ['status', 'started_at']
    search_fields = ['user__username', 'challenge__title']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['challenge', 'questions_count', 'time_limit']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_text', 'correct_answer']
    list_filter = ['quiz', 'correct_answer']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_questions', 'completed_at']
    list_filter = ['completed_at']