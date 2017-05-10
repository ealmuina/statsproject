import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'statsproject.settings')

import django
import datetime

django.setup()
from okcupid.models import *


def populate():
    q1 = add_question('Do you like Quidditch?')
    q2 = add_question('Are you good at defeating dark wizards?')

    m = add_gender('Male')
    f = add_gender('Female')

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
    add_answer(harry, q1, True, True, 10)
    add_answer(harry, q2, True, True, 100)

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
    add_answer(hermione, q1, True, False, 1)
    add_answer(hermione, q2, False, True, 250)


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
    u = User.objects.get_or_create(username=username)[0]
    u.first_name = first_name
    u.last_name = last_name
    u.email = email
    u.set_password(password)
    u.save()

    up = UserProfile.objects.get_or_create(user=u, gender=gender, birthday=birthday)[0]
    up.save()
    for g in liked_genders:
        up.liked_genders.add(g)
    up.save()
    return up


if __name__ == '__main__':
    print("Starting Statistics Project population script...")
    populate()

    # harry = UserProfile.objects.get(user__username='harry')
    # hermione = UserProfile.objects.get(user__username='hermione')
    #
    # print(UserProfile.match_percentage(harry, hermione))
