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
from functools import cached_property
from typing import List, Optional
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from .endpoints import BASE_URL
from .comic import Comic


class ComicList:

    """
    A class that represents a comic list.

    :param code: The comic list's code.
    :type code: :class:`int`
    :param infinity: Represents a maximum for internal usage; the higher this value, the better the results.
    :type infinity: Optional[:class:`int`]

    :ivar code: The comic list's code.
    :ivar title: The comic list's title.
    :ivar author: The comic list's author.
    :ivar date: The comic list's release date.
    :ivar formatted_date: A formatted version of the comic list's date.
    :ivar identifier: The comic list's identifier.
    :ivar description: The comic list's description.
    :ivar url: The comic list's URL.
    :ivar comics: A list containing comics from the comic list.

    .. warning::

        ``comics`` is heavy on resources when called for the first time.
    """

    def __init__(self, code: int, infinity: Optional[int] = 20) -> None:
        self.code = code
        self._infinity = infinity

        page = Request(f"{BASE_URL}comics/lists/{self.code}")
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        self.title = soup.find("h2", {"class": "h1"}).text
        self.author = soup.find("span", {"class": "h3"}).text[3:]
        self.formatted_date = list(soup.find("time", {"itemprop": "datePublished"}).children)[1].text
        self.date = datetime.strptime(self.formatted_date, "%B %d, %Y")
        self.url = soup.find("input", {"class": "js-copy-link form-control"}).attrs["value"]
        self.identifier = self.url.split("/")[-1]
        self.description = list(soup.find("section", {"class": "gc-article gc-gap-full"}).children)[1].text

    def __eq__(self, __o: ComicList) -> bool:
        return self.url == __o.url

    @cached_property
    def comics(self) -> List[Comic]:
        page = Request(f"{BASE_URL}comics/lists/{self.code}?page={self._infinity}")
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")
        comics = []
        tags = soup.find_all("div", {"class": "content-section-sm"})
        for tag in tags:
            comic = list(tag.children)[1].attrs["data-url"].split("/")[3:]
            comic = Comic(comic[0], datetime(int(comic[1]), int(comic[2]), int(comic[3])))
            if comic not in comics:
                comics.append(comic)
        return comics
