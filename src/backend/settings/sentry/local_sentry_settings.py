from .common_sentry_settings import SentrySettingsInterface


class SentrySettings(SentrySettingsInterface):
  address = 'localhost'
  port = '9000'
  protocol = 'http://'
  token_private = '55231385a5b6435380c943ffc71e097c'
  token_public = 'd51f4c915b7a41619ec7934371c685c7'
