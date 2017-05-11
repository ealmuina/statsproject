import math

from django.contrib.auth.models import User
from django.db import models


class Gender(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=160, unique=True)

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    gender = models.ForeignKey(Gender)
    liked_genders = models.ManyToManyField(Gender, related_name='+')

    birthday = models.DateField()
    picture = models.ImageField(upload_to='profile_images')

    @staticmethod
    def match_percentage(user1, user2):
        eval1 = MatchEvaluation.objects.get(evaluator=user1, evaluated=user2).value
        eval2 = MatchEvaluation.objects.get(evaluator=user2, evaluated=user1).value
        return math.sqrt(eval1 * eval2)

    def __str__(self):
        return self.user.username


class Answer(models.Model):
    WEIGHT_CHOICES = [
        (1, 'Not at all important'),
        (10, 'A little important'),
        (50, 'Somewhat important'),
        (100, 'Very important'),
        (250, 'Mandatory'),
    ]

    user = models.ForeignKey(UserProfile)
    question = models.ForeignKey(Question)

    value = models.BooleanField(default=False)
    liked_value = models.BooleanField(default=False)
    weight = models.IntegerField(choices=WEIGHT_CHOICES)

    class Meta:
        unique_together = ('user', 'question')


class MatchEvaluation(models.Model):
    evaluator = models.ForeignKey(UserProfile, related_name='+')
    evaluated = models.ForeignKey(UserProfile, related_name='+')

    value = models.FloatField(default=0)

    class Meta:
        unique_together = ('evaluator', 'evaluated')

    @staticmethod
    def evaluate(evaluator, evaluated):
        if evaluated.gender not in evaluator.liked_genders.iterator():
            return 0

        num, den = 0, 0
        for answer in evaluator.answer_set.iterator():
            other_answer = evaluated.answer_set.get(question=answer.question)
            num += answer.weight if other_answer.value == answer.liked_value else 0
            den += answer.weight

        return 100 * num / den

    def save(self, *args, **kwargs):
        self.value = self.evaluate(self.evaluator, self.evaluated)
        super(MatchEvaluation, self).save(*args, **kwargs)
