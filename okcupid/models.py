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
    user = models.OneToOneField(User, primary_key=True)
    gender = models.ForeignKey(Gender)
    liked_genders = models.ManyToManyField(Gender, related_name='+')

    birthday = models.DateField()
    picture = models.ImageField(upload_to='profile_images', null=True, blank=True)
    min_match = models.IntegerField()

    @staticmethod
    def match_percentage(user1, user2):
        eval1 = MatchEvaluation.objects.get(evaluator=user1, evaluated=user2).value
        eval2 = MatchEvaluation.objects.get(evaluator=user2, evaluated=user1).value
        return math.sqrt(eval1 * eval2)

    @staticmethod
    def current_profile(user):
        u = UserProfile.objects.get(user_id=user.id)
        return u

    def evaluate(self, evaluated):
        if evaluated.gender not in self.liked_genders.iterator():
            return 0

        num, den = 0, 0
        for answer in self.answer_set.iterator():
            other_answer = evaluated.answer_set.get(question=answer.question)
            num += answer.weight if other_answer.value == answer.liked_value else 0
            den += answer.weight

        return 100 * num / den

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

    # TODO: Dar la opcion de descartar y que no aparezca mas en las listas. Un campo para esto

    class Meta:
        unique_together = ('evaluator', 'evaluated')

    @staticmethod
    def matches_for(user_id):
        min_val = UserProfile.objects.get(user_id=user_id).min_match
        m1 = MatchEvaluation.objects.filter(evaluated_id=user_id, value__gte=min_val)
        m2 = MatchEvaluation.objects.filter(evaluator_id=user_id, value__gte=min_val)
        return m1.union(m2).order_by('-value')

    def matched_user(self, user_id):
        if self.evaluator_id == user_id:
            return self.evaluated
        elif self.evaluated_id == user_id:
            return self.evaluator
        return None

    def save(self, *args, **kwargs):
        self.value = self.evaluator.evaluate(self.evaluated)
        super(MatchEvaluation, self).save(*args, **kwargs)


class Opinion(models.Model):
    user = models.ForeignKey(UserProfile)

    text = models.TextField(max_length=300)

    def __str__(self):
        return self.text


class Message(models.Model):
    from_u = models.ForeignKey(UserProfile, related_name='+')
    to_u = models.ForeignKey(UserProfile, related_name='+')

    text = models.CharField(max_length=600)
    read = models.BooleanField(default=False)
    sent = models.DateTimeField(auto_created=True)


class SentQuestion(models.Model):
    sender = models.ForeignKey(UserProfile)

    question = models.CharField(max_length=250)
    accepted = models.NullBooleanField(null=True, default=None)

    def __str__(self):
        return self.question
