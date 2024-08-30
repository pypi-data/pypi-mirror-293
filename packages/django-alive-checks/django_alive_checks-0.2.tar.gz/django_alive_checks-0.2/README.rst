

django-alive-checks
===================

.. image:: https://img.shields.io/pypi/v/django-alive-checks.svg
   :target: https://pypi.org/project/django-alive-checks/
   :alt: PyPI version

.. image:: https://github.com/PetrDlouhy/django-alive-checks/workflows/Django%20Tests/badge.svg
   :target: https://github.com/PetrDlouhy/django-alive-checks/actions
   :alt: Build status

`django-alive-checks` is a Django application that provides additional health checks for your Django projects. These checks are designed to work with the `django-alive <https://github.com/pinax/django-alive>`_ package but include dependencies that cannot be part of `django-alive` itself.

Installation
------------

You can install the base package with:

.. code-block:: bash

    pip install django-alive-checks

If you want to include support for Elasticsearch, install with:

.. code-block:: bash

    pip install django-alive-checks[elasticsearch]


Integration with django-alive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To integrate the ``check_elasticsearch`` function with your ``django-alive`` checks, you can add it to your health checks configuration:

.. code-block:: python

    # settings.py

    ALIVE_CHECKS = [
        ...
        ("alive_checks.checks.check_elasticsearch", {"settings": ES_SETTINGS}),
    ]

Where the ``ES_SETTINGS`` contains settings that you pass to ``elsaticsearch.Elasticsearch``.


Testing
-------

To run the tests for this project:

.. code-block:: bash

    python -m unittest discover

The tests cover the following scenarios:

- Successful connection to Elasticsearch.
- Failed connection to Elasticsearch.
- Exceptions during connection attempts.
- Handling the absence of the ``elasticsearch`` package.

Contributing
------------

Contributions are welcome! If you encounter any issues, have ideas for improvements, or want to add more checks, feel free to open an issue or submit a pull request.

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for more details.

Acknowledgments
---------------

Thanks to the Django and Elasticsearch communities for their continued support and development of the libraries that make this project possible.

