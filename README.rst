.. image:: https://raw.githubusercontent.com/Ombucha/gocomics.py/main/banner.png

.. image:: https://img.shields.io/pypi/v/gocomics.py
    :target: https://pypi.python.org/pypi/gocomics.py
    :alt: PyPI version
.. image:: https://static.pepy.tech/personalized-badge/gocomics.py?period=total&left_text=downloads&left_color=grey&right_color=red
    :target: https://pypi.python.org/pypi/gocomics.py
    :alt: PyPI downloads
.. image:: https://sloc.xyz/github/Ombucha/gocomics.py?lower=True
    :target: https://github.com/Ombucha/gocomics.py/graphs/contributors
    :alt: Lines of code
.. image:: https://img.shields.io/github/repo-size/Ombucha/gocomics.py?color=yellow
    :target: https://github.com/Ombucha/gocomics.py
    :alt: Repository size

**gocomics.py** is a Pythonic, fun, and easy-to-use library for fetching comics and metadata from GoComics.com. Whether you want to build a comic reader, analyze trends, or just grab your favorite strip, this package is for you!

Features
--------

- Fetch any comic by identifier and date
- Get comic metadata (title, author, description, images, etc.)
- List all available comics and categories
- Find popular and political comics
- Fully documented and type-annotated
- MIT licensed and open source

Why gocomics.py?
----------------

- **Simple**: One-liner to fetch a comic!
- **Powerful**: Access all the metadata you need
- **Community-driven**: Contributions welcome
- **Inspired by comics**: Because code should be fun!

Background
----------

In 2024, GoComics.com changed its interface and added a paywall that blocks most comics from non-subscribers. gocomics.py works by programmatically fetching comic data and images, allowing you to access comics and metadata even if they are paywalled on the site.

Requirements
------------

- Python 3.8+
- `beautifulsoup4 <https://pypi.python.org/pypi/beautifulsoup4>`_
- `requests <https://pypi.python.org/pypi/requests>`_

Installation
------------

.. code-block:: sh

    # Stable release
    python3 -m pip install "gocomics.py"  # Unix/macOS
    py -m pip install "gocomics.py"       # Windows

.. code-block:: sh

    # Development version
    git clone https://github.com/Ombucha/gocomics.py

Comic API
---------

- :class:`gocomics.Comic` – Fetch and explore a comic
    - `identifier` (str): The comic's identifier (e.g., "calvinandhobbes")
    - `date` (datetime, optional): The date of the comic (default: latest)
    - `.title`, `.description`, `.image_url`, `.author`, `.followers_count`, `.about`, `.characters`, etc.
    - `.download(filename=None, path=None)`: Download the comic image
    - `.show(filename=None, path=None)`: Open the comic image in your default viewer
    - `.refresh()`: Refresh the comic's data
- :func:`gocomics.search` – List all comics (optionally filter by category or updated today)
- :func:`gocomics.search_political` – List political comics (optionally filter by category or updated today)
- :func:`gocomics.get_popular_comics` – Get trending/popular comics (optionally political)
- :func:`gocomics.stream_comics` – Iterate comics for a strip between two dates

**RETRY_COUNT**
~~~~~~~~~~~~~~

`RETRY_COUNT` is a module-level constant in `comic.py` that controls how many times the parser will attempt to extract the comic image from the page. If you encounter issues with missing images, try increasing this value.

Examples
--------

**Basic usage:**

.. code-block:: python

    from gocomics import Comic
    comic = Comic("calvinandhobbes")
    print(comic.title)
    print(comic.image_url)

**Fetch a comic from a specific date:**

.. code-block:: python

    from datetime import datetime
    comic = Comic("garfield", datetime(2020, 1, 1))
    print(comic.title, comic.image_url)

**Download and show a comic:**

.. code-block:: python

    path = comic.download(filename="garfield2020.png")
    comic.show(filename="garfield2020.png")

**Refresh comic data:**

.. code-block:: python

    comic.refresh()

**List all available comic identifiers:**

.. code-block:: python

    from gocomics.utils import search
    all_comics = search()
    print(all_comics[:10])  # Show first 10

**List comics in a category:**

.. code-block:: python

    animal_comics = search(categories=["funny-animals"])
    print(animal_comics)

**List comics updated today:**

.. code-block:: python

    updated_today = search(last_updated_today=True)
    print(updated_today)

**List political comics:**

.. code-block:: python

    from gocomics.utils import search_political
    political = search_political()
    print(political)

**List popular comics:**

.. code-block:: python

    from gocomics.utils import get_popular_comics
    popular = get_popular_comics()
    print(popular)

**List popular political comics:**

.. code-block:: python

    popular_political = get_popular_comics(political=True)
    print(popular_political)

**Stream all comics for a strip between two dates:**

.. code-block:: python

    from gocomics.utils import stream_comics
    from datetime import datetime
    for comic in stream_comics("garfield", start_date=datetime(2020, 1, 1), end_date=datetime(2020, 1, 5)):
        print(comic.date, comic.title)

See the `Documentation <https://gocomics.readthedocs.io/>`_ for full API details.

Contributing
------------

We love contributions! Please see `CONTRIBUTING.md <https://github.com/Ombucha/gocomics.py/blob/main/CONTRIBUTING.md>`_ for guidelines. Lint with `pylint`, follow PEP 8, and open a PR!

Support & Community
-------------------

- Found a bug? Open an issue on GitHub.
- Questions? Join the discussions.
- Be kind and have fun - see our Code of Conduct.

Links
-----

- `GoComics <https://gocomics.com/>`_
- `Documentation <https://gocomics.readthedocs.io/>`_
- `PyPI <https://pypi.org/project/gocomics.py/>`_

License
-------

MIT License. See `LICENSE <https://github.com/Ombucha/gocomics.py/blob/main/LICENSE`_.
