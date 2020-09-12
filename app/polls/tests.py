import datetime

from django.test import TestCase

# Create your tests here.
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertNotEquals(future_question.was_published_recently(), False)