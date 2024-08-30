import logging

from django.core.exceptions import ImproperlyConfigured

try:
    from elasticsearch import Elasticsearch
except ImportError:
    Elasticsearch = None


class HealthcheckFailure(Exception):
    pass


log = logging.getLogger(__name__)


def check_elasticsearch(settings=None):
    # type: (dict) -> None
    """
    Ping the Elasticsearch server to verify it's reachable
    :param dict settings: Elasticsearch settings
    :return None:
    """
    if Elasticsearch is None:
        raise ImproperlyConfigured("elasticsearch package is not installed")

    if settings is None:
        settings = {}

    try:
        ping = Elasticsearch(**settings).ping()
    except Exception:
        log.exception("Elasticsearch connection failed")
        raise HealthcheckFailure("Elasticsearch exception")
    if not ping:
        log.error("Elasticsearch ping failed")
        raise HealthcheckFailure("Elasticsearch error")
