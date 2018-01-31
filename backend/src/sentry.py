import logging

from raven import Client as Raven
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging

from settings.sentry.local_sentry_settings import SentrySettings


def initialize_sentry():
  client = Raven(SentrySettings.getURL())
  client.tags_context({
    'Aspect': 'Backend',
    'Language': 'Python',
    'logger': 'python'
  })

  handler = SentryHandler(client)
  handler.setLevel(logging.ERROR)
  setup_logging(handler)

  return client
