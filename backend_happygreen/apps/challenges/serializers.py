from rest_framework import serializers
from .models import Challenge, UserChallenge, Quiz, QuizQuestion, QuizAttempt
from apps.authentication.serializers import UserProfileSerializer

class ChallengeSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'challenge_type', 'difficulty',
                 'points_reward', 'target_count', 'is_active', 'start_date',
                 'end_date', 'is_completed', 'user_progress', 'created_at']

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                user_challenge = UserChallenge.objects.get(user=request.user, challenge=obj)
                return user_challenge.status == 'completed'
            except UserChallenge.DoesNotExist:
                return False
        return False

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                user_challenge = UserChallenge.objects.get(user=request.user, challenge=obj)
                return {
                    'progress': user_challenge.progress,
                    'target': obj.target_count,
                    'status': user_challenge.status
                }
            except UserChallenge.DoesNotExist:
                return {
                    'progress': 0,
                    'target': obj.target_count,
                    'status': 'not_started'
                }
        return None

class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = UserChallenge
        fields = ['id', 'user', 'challenge', 'status', 'progress',
                 'completed_at', 'started_at']

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d']
        # Non esporre la risposta corretta

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)
    challenge = ChallengeSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'challenge', 'questions_count', 'time_limit', 'questions']

class QuizSubmissionSerializer(serializers.Serializer):
    answers = serializers.DictField(child=serializers.CharField())

    def validate_answers(self, value):
        # Valida che le risposte siano nel formato corretto
        for question_id, answer in value.items():
            if answer not in ['A', 'B', 'C', 'D']:
                raise serializers.ValidationError(f"Invalid answer '{answer}' for question {question_id}")
        return value

class QuizAttemptSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    quiz = QuizSerializer(read_only=True)

    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'quiz', 'score', 'total_questions', 'completed_at']
