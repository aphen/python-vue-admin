from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Question, Choice
from .serializers import QuestionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-pub_date')
    serializer_class = QuestionSerializer

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        question = self.get_object()
        try:
            choice_id = request.data.get('choice')
            choice = get_object_or_404(Choice, pk=choice_id, question=question)
            choice.votes += 1
            choice.save()
            return Response({'status': 'vote recorded'})
        except (KeyError, Choice.DoesNotExist):
            return Response({'error': 'Invalid choice'}, status=status.HTTP_400_BAD_REQUEST)