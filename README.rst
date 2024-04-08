==============================================
web3.py example app for eth payments in django
==============================================

In this repository, we take a `Django Web Framework`_ project.
We create an application with two models (data stored in a database).

.. code:: python

    class Order(models.Model):
        ...

    class Payment(models.Model):
        ...

.. _Django Web Framework: https://docs.djangoproject.com/en/5.0/

Use a django built-in admin frontend. And add little bit of `web3.py`_ flavour
to interface with `Ethereum blockchain`_.

.. _web3.py: https://web3py.readthedocs.io/en/stable/index.html
.. _Ethereum blockchain: https://ethereum.org/en/

install
~~~~~~~

::

  python -m venv PY
  source PY/bin/activate
  pip install -r requirements.txt
  ./manage.py migrate
  ./manage.py runserver

