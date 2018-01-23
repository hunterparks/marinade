from abc import ABCMeta


class SentrySettingsInterface:
  __metaclass_ = ABCMeta

  address = None
  port = None
  protocol = None
  token_private = None
  token_public = None

  @classmethod
  def getURL(cls):
    if cls.address and cls.port and cls.protocol and cls.token_private and cls.token_public:
      return cls.protocol + cls.token_public + ':' + cls.token_private + '@' + cls.address + ':' + cls.port + '/1'
    return None

'''

  _______________________
  USING SENTRY SETTINGS:
  _______________________

    Create a class implementation in a file in this directory called local_sentry_settings.py.
    An example configuration is below.

  -----------------------
  EXAMPLE CONFIGURATION:
  -----------------------

    from .common_sentry_settings import SentrySettingsInterface
  
  
    class SentrySettings(SentrySettingsInterface):
      address = 'localhost'
      port = '9000'
      protocol = 'http://'
      token_private = 'e74d0f617b0d4d76a4c1acd19d20da6c'
      token_public = '3d4bca0e8aa8465bae6fd29934f5ea0f'

'''
