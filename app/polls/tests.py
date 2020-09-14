import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient

# from accounts.models import User
from accounts.views import TestGenericView
from polls.models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# with APIRequestFactory()
class TestGenericTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create(first_name='test_jh', last_name='test_lee', email='test0@test0.com')

    def test_authenticate_with_user(self):
        request = self.factory.get('/test/')
        force_authenticate(request, user=self.user)
        response = TestGenericView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_authenticate_without_user(self):
        request = self.factory.get('/test/')
        response = TestGenericView.as_view()(request)
        self.assertEqual(response.status_code, 401)


# with APIClient
class TestGenericTestWithAPIClient(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='jh', email='test@test.com', password='test1234')
        self.client = APIClient()

    def test_authenticate_with_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/test/')
        # response = TestGenericView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_authenticate_without_user(self):
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 401)

