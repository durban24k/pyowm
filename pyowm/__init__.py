#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyowm import constants
from pyowm.config import DEFAULT_CONFIG
from pyowm.utils import timestamps, strings


strings.check_if_running_with_python_2()


def OWM(API_key=DEFAULT_CONFIG['api_key'], version=constants.WEATHER_API_VERSION,
        config_module=None, language=None, subscription_type=None, use_ssl=None):
    """
    A parametrized factory method returning a global OWM instance that
    represents the desired OWM Weather API version (or the currently supported one
    if no version number is specified)

    :param API_key: the OWM Weather API key (defaults to a test value)
    :type API_key: str
    :param version: the OWM Weather API version. Defaults to ``None``, which means
        use the latest web API version
    :type version: tuple
    :param config_module: the Python path of the configuration module you want
        to provide for instantiating the library. Defaults to ``None``, which
        means use the default configuration values for the web API version
        support you are currently requesting. Please be aware that malformed
        user-defined configuration modules can lead to unwanted behaviour!
    :type config_module: str (eg: 'mypackage.mysubpackage.myconfigmodule')
    :param language: the language in which you want text results to be returned.
          It's a two-characters string, eg: "en", "ru", "it". Defaults to:
          ``None``, which means use the default language.
    :type language: str
    :param subscription_type: the type of OWM Weather API subscription to be wrapped.
           Can be 'free' (free subscription) or 'pro' (paid subscription),
           Defaults to: 'free'
    :type subscription_type: str
    :param use_ssl: whether API calls should be made via SSL or not.
           Defaults to: False
    :type use_ssl: bool
    :returns: an instance of a proper *OWM* subclass
    :raises: *ValueError* when unsupported OWM API versions are provided
    """
    if version == (2, 5, 0):
        if config_module is None:
            config_module = "pyowm.weatherapi25.configuration25"
        cfg_module = __import__(config_module,  fromlist=[''])
        from pyowm.weatherapi25.owm25 import OWM25
        if language is None:
            language = cfg_module.language
        if subscription_type is None:
            subscription_type = cfg_module.API_SUBSCRIPTION_TYPE
            if subscription_type not in ['free', 'pro']:
                subscription_type = 'free'
        if use_ssl is None:
            use_ssl = cfg_module.USE_SSL
        return OWM25(cfg_module.parsers, API_key, cfg_module.cache,
                     language, subscription_type, use_ssl)
    raise ValueError("Unsupported OWM Weather API version")
