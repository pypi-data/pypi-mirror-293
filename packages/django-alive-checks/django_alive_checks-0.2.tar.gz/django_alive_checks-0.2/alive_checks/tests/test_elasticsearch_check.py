from unittest import TestCase, mock

from django.core.exceptions import ImproperlyConfigured

from alive_checks.checks import HealthcheckFailure, check_elasticsearch


class ElasticsearchCheckTests(TestCase):

    @mock.patch("alive_checks.checks.elasticsearch.Elasticsearch")
    def test_elasticsearch_ping_success(self, mock_elasticsearch):
        mock_elasticsearch.return_value.ping.return_value = True
        try:
            check_elasticsearch()
        except HealthcheckFailure:
            self.fail("HealthcheckFailure raised unexpectedly")

    @mock.patch("alive_checks.checks.elasticsearch.Elasticsearch")
    def test_elasticsearch_ping_failure(self, mock_elasticsearch):
        mock_elasticsearch.return_value.ping.return_value = False
        with self.assertRaises(HealthcheckFailure):
            check_elasticsearch()

    @mock.patch("alive_checks.checks.elasticsearch.Elasticsearch")
    def test_elasticsearch_exception(self, mock_elasticsearch):
        mock_elasticsearch.side_effect = Exception("Connection failed")
        with self.assertRaises(HealthcheckFailure):
            check_elasticsearch()
