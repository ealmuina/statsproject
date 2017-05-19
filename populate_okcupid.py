import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'statsproject.settings')

import django
import datetime

django.setup()
from okcupid.models import *


def populate():
    questions = [
        'Do you smoke?',
        'Do you enjoy discussing politics?',
        'Is religion/God important in your life?',
        'Does the word "carefree" describe you?',
        'Does the word "intense" describe you?',
        'Do you want your next relationship to last for a long time?',
        'Do you drink alcohol?',
        'Could you date someone who was really messy?',
        'Do you consider "kissing in Paris" to be more romantic than "kissing in a tent, in the woods"?',
        'Are you currently employed?',
        'Do you consider yourself "weird" rather than "normal"?',
        'Is jealousy healthy in a relationship?',
        'Would you date someone who was in considerable debt?',
        'Is astrological sign at all important in a match?',
        'Would you strongly prefer to date someone of your own skin color / racial background?',
        'Is a Sci-Fi Convention an event that sounds appealing to you?',
        'Is a Political Convention an event that sounds appealing to you?',
        'Is a Music Festival an event that sounds appealing to you?',
        'Is a New Years Eve in Times Square an event that sounds appealing to you?',
    ]
    questions = [add_question(q) for q in questions]

    m = add_gender('Male')
    f = add_gender('Female')
    o = add_gender('Other')

    harry = add_user(
        username='harry',
        first_name='Harry',
        last_name='Potter',
        birthday=datetime.date(1980, 7, 31),
        gender=m,
        liked_genders=[f],
        email='potter@hogwarts.co.uk',
        password='1234'
    )
    add_answer(harry, questions[0], True, True, 10)
    add_answer(harry, questions[1], True, True, 100)

    hermione = add_user(
        username='hermione',
        first_name='Hermione',
        last_name='Granger',
        birthday=datetime.date(1979, 9, 19),
        gender=f,
        liked_genders=[m],
        email='hgranger@hogwarts.co.uk',
        password='1234'
    )
    add_answer(hermione, questions[0], True, False, 1)
    add_answer(hermione, questions[1], False, True, 250)

    make_evaluations()


def add_answer(user, question, value, liked_value, weight):
    a = Answer.objects.get_or_create(user=user, question=question, weight=weight)[0]
    a.value = value
    a.liked_value = liked_value
    a.save()
    return a


def add_gender(name):
    g = Gender.objects.get_or_create(name=name)[0]
    g.save()
    return g


def add_question(text):
    q = Question.objects.get_or_create(text=text)[0]
    q.save()
    return q


def add_user(username, first_name, last_name, birthday, gender, liked_genders, email, password):
    # Create Django User
    u = User.objects.get_or_create(username=username)[0]
    u.first_name = first_name
    u.last_name = last_name
    u.email = email
    u.set_password(password)
    u.save()

    # Create UserProfile
    up = UserProfile.objects.get_or_create(user=u, gender=gender, birthday=birthday)[0]
    up.save()
    for g in liked_genders:
        up.liked_genders.add(g)
    up.save()
    return up


def make_evaluations():
    for u1 in UserProfile.objects.all():
        for u2 in UserProfile.objects.exclude(id=u1.id):
            MatchEvaluation.objects.get_or_create(evaluator=u1, evaluated=u2)[0].save()
            MatchEvaluation.objects.get_or_create(evaluator=u2, evaluated=u1)[0].save()


if __name__ == '__main__':
    print("Starting Statistics Project population script...")
    populate()
