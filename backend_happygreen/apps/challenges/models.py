from django.db import models
from apps.authentication.models import CustomUser


class Challenge(models.Model):
    CHALLENGE_TYPES = [
        ('scan_objects', 'Scan Objects'),
        ('quiz', 'Quiz'),
        ('recycling', 'Recycling'),
        ('exploration', 'Exploration'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=50, choices=CHALLENGE_TYPES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='easy')
    points_reward = models.IntegerField(default=10)
    target_count = models.IntegerField(default=1)  # Es. scansiona 10 oggetti
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'challenge']

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"


class Quiz(models.Model):
    challenge = models.OneToOneField(Challenge, on_delete=models.CASCADE, related_name='quiz')
    questions_count = models.IntegerField(default=5)
    time_limit = models.IntegerField(help_text="Time limit in minutes", default=10)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Question for {self.quiz.challenge.title}"


class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.challenge.title} - {self.score}/{self.total_questions}"
