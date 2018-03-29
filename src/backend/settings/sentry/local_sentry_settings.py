from .common_sentry_settings import SentrySettingsInterface


class SentrySettings(SentrySettingsInterface):
  address = '192.168.64.2'
  port = '9000'
  protocol = 'http://'
  token_private = 'e74d0f617b0d4d76a4c1acd19d20da6c'
  token_public = '3d4bca0e8aa8465bae6fd29934f5ea0f'
