"""
MIT License

Copyright (c) 2022 Omkaar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import annotations

from datetime import datetime
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from typing import List, Literal, Optional

from bs4 import BeautifulSoup
from requests.utils import requote_uri

from .endpoints import BASE_URL
from .comic import Comic


def fetch_comics(*, category: Optional[str] = None) -> List[str]:
    """
    Fetches a list of comic URL slugs.

    :param category: The comic category.
    :type category: :class:`str`
    """
    slugs = []
    if category is None:
        page = Request(f"{BASE_URL}comics/a-to-z")
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")
        tags = soup.find_all("a", {"class": "gc-blended-link gc-blended-link--primary col-12 col-sm-6 col-lg-4"}, href = True)
        for tag in tags:
            path = urlparse(tag.attrs["href"]).path
            slugs.append(path.split("/")[1])
    else:
        page = Request(f"{BASE_URL}/comics/{category.lower()}")
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")
        tags = soup.find_all("a", {"class": "gc-blended-link gc-blended-link--primary"}, href = True)
        for tag in tags:
            path = urlparse(tag.attrs["href"]).path
            slugs.append(path.split("/")[1])
    return slugs


def search(text: str, *, category: Optional[Literal["comic", "feature"]] = "comic", page: Optional[int] = 1, sort: Optional[Literal["relevance", "ascending", "descending"]] = "relevance") -> List[Comic]:
    """
    Searches GoComics.

    :param text: The text to search for.
    :type text: str
    :param category: The category to search in.
    :type category: Optional[Literal["comic", "feature"]]
    :param page: The page number.
    :type page: Optional[:class:`int`]
    :param sort: The method of sorting results (based on date).
    :type sort: Optional[Literal["ascending", "descending"]]
    """
    sorts = {"relevance": "relevance", "ascending": "date_asc", "descending": "date_desc"}
    url = requote_uri(f"{BASE_URL}search/full_results?category={category.lower()}&terms={text}&page={page}&sort={sorts[sort.lower()]}")
    page = Request(url)
    with urlopen(page) as result:
        soup = BeautifulSoup(result.read(), "html.parser")
    comics = []
    if category == "comic":
        tags = soup.find_all("a", {"itemprop": "image"}, href = True)
        for tag in tags:
            path = tag.attrs["href"].split("/")
            comics.append(Comic(path[1], datetime(int(path[2]), int(path[3]), int(path[4]))))
    else:
        tags = soup.find_all("div", {"class": "content-section-sm"})
        for tag in tags:
            path = urlparse(list(tag.children)[1].attrs["href"]).path.replace("/", "")
            comics.append(Comic(path, random = True))
    return comics
