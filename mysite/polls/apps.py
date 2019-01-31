from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'
    verbose_name = "My Polls Application"

    # Run this method once when Django starts up
    # https://code.i-harness.com/en/q/dd8201
    #
    # NOTE: Method must be named 'ready'
    # def ready(self):
    #     print ('Hello you, world')
