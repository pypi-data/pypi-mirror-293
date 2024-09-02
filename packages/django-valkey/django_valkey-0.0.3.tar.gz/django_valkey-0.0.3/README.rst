===============================
Valkey cache backend for Django
===============================

Introduction
------------

django-valkey-backend is a new project aiming to bring full valkey support for django.
currently it's an exact copy of django's own backend for Redis, only modified to work with valkey.



Requirements
~~~~~~~~~~~~

- `Python`_ 3.10+
- `Django`_ 5.1+ (it probably works with lower versions as well, just haven't test it)
- `valkey-py`_ 6.0.0+
- `Valkey server`_ 2.8+ (again, probably works with ower versions too)

.. _Python: https://www.python.org/downloads/
.. _Django: https://www.djangoproject.com/download/
.. _valkey-py: https://pypi.org/project/valkey/
.. _Valkey server: https://valkey.io/download/

User guide
----------

Installation
~~~~~~~~~~~~

Install with pip:

.. code-block:: console

    $ python -m pip install django-valkey

Install with c bindings for Maximum performance:

.. code-block:: console

    $ python -m pip install django-valkey[libvalkey]

Configure as cache backend
~~~~~~~~~~~~~~~~~~~~~~~~~~

To start using django-redis, you should change your Django cache settings to
something like:

.. code-block:: python

    CACHES = {
        "default": {
            "BACKEND": "django_valkey.backend.ValkeyCache",
            "LOCATION": "valkey://127.0.0.1:6379",
        }
    }


as i said this backend is an exact copy of django's own redis backend and works exactly the same:
https://docs.djangoproject.com/en/5.1/topics/cache/#redis

just replace `redis` with `valkey` when you see