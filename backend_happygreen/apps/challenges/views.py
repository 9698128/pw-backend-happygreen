from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Challenge, UserChallenge, Quiz, QuizQuestion, QuizAttempt
from .serializers import (
    ChallengeSerializer, UserChallengeSerializer, QuizSerializer,
    QuizSubmissionSerializer, QuizAttemptSerializer
)


class ActiveChallengesView(generics.ListAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        return Challenge.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).order_by('-created_at')


class UserChallengesView(generics.ListAPIView):
    serializer_class = UserChallengeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserChallenge.objects.filter(user=self.request.user).order_by('-started_at')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_challenge(request, challenge_id):
    try:
        challenge = get_object_or_404(Challenge, id=challenge_id, is_active=True)

        # Controlla se l'utente ha già iniziato questa sfida
        user_challenge, created = UserChallenge.objects.get_or_create(
            user=request.user,
            challenge=challenge,
            defaults={'status': 'in_progress'}
        )

        if not created:
            return Response({'error': 'Challenge already started'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserChallengeSerializer(user_challenge)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Challenge.DoesNotExist:
        return Response({'error': 'Challenge not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_challenge_progress(request, challenge_id):
    try:
        user_challenge = get_object_or_404(
            UserChallenge,
            user=request.user,
            challenge_id=challenge_id
        )

        increment = request.data.get('increment', 1)
        user_challenge.progress += increment

        # Controlla se la sfida è completata
        if user_challenge.progress >= user_challenge.challenge.target_count:
            user_challenge.status = 'completed'
            user_challenge.completed_at = timezone.now()

            # Assegna punti eco all'utente
            request.user.eco_points += user_challenge.challenge.points_reward
            request.user.level = (request.user.eco_points // 100) + 1
            request.user.save()

            # Controlla per nuovi badge
            from apps.authentication.views import check_and_award_badges
            check_and_award_badges(request.user)

        user_challenge.save()

        serializer = UserChallengeSerializer(user_challenge)
        return Response(serializer.data)

    except UserChallenge.DoesNotExist:
        return Response({'error': 'User challenge not found'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_quiz(request, challenge_id):
    try:
        challenge = get_object_or_404(Challenge, id=challenge_id, challenge_type='quiz')
        quiz = get_object_or_404(Quiz, challenge=challenge)

        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    except (Challenge.DoesNotExist, Quiz.DoesNotExist):
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, challenge_id):
    try:
        challenge = get_object_or_404(Challenge, id=challenge_id, challenge_type='quiz')
        quiz = get_object_or_404(Quiz, challenge=challenge)

        serializer = QuizSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers = serializer.validated_data['answers']

        # Calcola il punteggio
        correct_answers = 0
        total_questions = quiz.questions.count()

        for question_id, user_answer in answers.items():
            try:
                question = QuizQuestion.objects.get(id=question_id, quiz=quiz)
                if question.correct_answer == user_answer:
                    correct_answers += 1
            except QuizQuestion.DoesNotExist:
                continue

        # Salva il tentativo
        quiz_attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=correct_answers,
            total_questions=total_questions
        )

        # Aggiorna il progresso della sfida se il punteggio è sufficiente (>= 60%)
        if correct_answers / total_questions >= 0.6:
            user_challenge, created = UserChallenge.objects.get_or_create(
                user=request.user,
                challenge=challenge,
                defaults={'status': 'in_progress'}
            )

            user_challenge.progress = 1
            user_challenge.status = 'completed'
            user_challenge.completed_at = timezone.now()
            user_challenge.save()

            # Assegna punti eco
            request.user.eco_points += challenge.points_reward
            request.user.level = (request.user.eco_points // 100) + 1
            request.user.save()

        return Response({
            'score': correct_answers,
            'total_questions': total_questions,
            'percentage': round((correct_answers / total_questions) * 100, 2),
            'passed': correct_answers / total_questions >= 0.6,
            'points_earned': challenge.points_reward if correct_answers / total_questions >= 0.6 else 0
        })

    except (Challenge.DoesNotExist, Quiz.DoesNotExist):
        return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
