import random
from string import ascii_lowercase, ascii_uppercase

from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from quips.models import Quip

# create random data for the quips
available_chars = ascii_lowercase + ascii_uppercase
content = [
    "".join([random.choice(available_chars) for _ in range(359)]) for _ in range(9)
]


class QuipModelTestCase(TestCase):
    def setUp(self):
        """ create three random users and quips """
        j = 0
        for i in range(3):
            user = User.objects.create(
                username="user%d" % i,
                email="user%d@user.com" % i,
                password="user%d" % i,
            )
            for _ in range(3):
                Quip.objects.create(user=user, content=content[j])
                j += 1

    def test_number_quips(self):
        self.assertEqual(len(Quip.objects.all()), 9)

    def test_quips_save(self):
        for i in range(1, 10):
            self.assertEqual(content[i - 1], Quip.objects.get(pk=i).content)

    def test_quips_order_correct(self):
        quips = Quip.objects.all()
        for i in range(1, 9):
            self.assertTrue(quips[i].created_at < quips[i - 1].created_at)

    def test_quip_text_length(self):
        """This will fail on Sqlite, which does nto enforce lengths on charfield"""
        user = User.objects.get(pk=random.randint(1, 3))
        with self.assertRaises(IntegrityError):
            Quip.objects.create(
                user=user,
                content="".join([random.choice(available_chars) for _ in range(380)]),
            )

    def test_quip_no_user(self):
        with self.assertRaises(IntegrityError):
            Quip.objects.create(
                user=None,
                content="".join([random.choice(available_chars) for _ in range(320)]),
            )
