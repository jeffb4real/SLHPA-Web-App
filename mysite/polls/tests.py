import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# tutorial05
from django.urls import reverse

################################
# For more info on all the asserts available in django.test.Testcase,
# $ python manage.py shell
# >>> from django.test import TestCase
# >>> dir(TestCase())
###############################

# Running tests does not affect our actual database:
# Creating test database for alias 'default'...
# [...]
# Destroying test database for alias 'default'...



# tutorial05
# Test methods must reside within a class that is a subclass
# of django.test.TestCase; and must begin with keyword 'test'
# 
# Here we have created a django.test.TestCase subclass.
#
# To run tests:
# $ python manage.py test polls
#
# What happened is this:
# - manage.py test polls looked for tests in the polls application
# - it found a subclass of the django.test.TestCase class
# - it created a special database for the purpose of testing
# - it looked for test methods - ones whose names begin with test
# - in test_was_published_recently_with_future_question it created a Question instance
#   whose pub_date field is 30 days in the future
# ...and using the assertIs() method, it discovered that its was_published_recently()
#   returns True, though we wanted it to return False
# The test informs us which test failed and even the line on which the failure occurred.
class QuestionModelTests(TestCase):

    # This test creates a Question instance with a pub_date in the future.
    # We then check the output of
    # was_published_recently() - which ought to be False.
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        #print ("test1")
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # Additional test case: older pub date
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        #print ("test2")
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    # Additional test case: recent pub date
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day (23 hrs + 59 min + 59 sec).
        """
        #print ("test3")
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

######################
# tutorial05
# Testing our new index view (updated IndexView class in polls/views.py)

# Helper function for our new test cases
# *NOTE*: Any questions created here will not be committed to our database.
#   "The database is reset for each test method, so the first question is no
#    longer there, and so again the index shouldn’t have any questions in it."
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


######################
# tutorial05
# Testing our new detail view (updated DetailView class in polls/views.py)
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)



