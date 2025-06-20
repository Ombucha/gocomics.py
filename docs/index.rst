gocomics.py
==========

Installation
------------

**Python 3.8 or higher is required.**

To install the stable version, do the following:

.. code-block:: sh

    # Unix / macOS
    python3 -m pip install "gocomics.py"

    # Windows
    py -m pip install "gocomics.py"


To install the development version, do the following:

.. code-block:: sh

    $ git clone https://github.com/Ombucha/gocomics.py

Make sure you have the latest version of Python installed, or if you prefer, a Python version of 3.8 or greater.

If you have have any other issues feel free to search for duplicates and then create a new issue on GitHub with as much detail as possible. Include the output in your terminal, your OS details and Python version.


Comic
-----

.. autoclass:: gocomics.Comic
    :members:


Other Functions
---------------

.. autofunction:: gocomics.search
.. autofunction:: gocomics.search_political
.. autofunction:: gocomics.get_popular_comics
.. autofunction:: gocomics.stream_comics