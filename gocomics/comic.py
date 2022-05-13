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


from datetime import datetime
from json import load
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from typing import List, Optional

from bs4 import BeautifulSoup


GOCOMICS_BASE_URL = "https://gocomics.com/"


class Comic:

    """
    A class that represents a comic.

    :param identifier: The comic's identifier.
    :type identifier: :class:`str`
    :param date: The comic's date.
    :type date: Optional[:class:`datetime`]
    :param random: Whether to choose a random comic, or not.
    :type random: Optional[:class:`bool`]

    .. note::

        If ``random`` is ``True``, ``date`` must not be specified.

    :ivar accountable_person: The person accountable for the comic.
    :ivar avatar: The url of the comic avatar.
    :ivar calendar: A list containing comics released in that month.
    :ivar code: The code associated with the comic.
    :ivar creator: The creator of the comic.
    :ivar date: The comic's date
    :ivar feature_id: The comic's feature ID.
    :ivar formatted_date: A formatted version of the comic's date.
    :ivar identifier: The comic's identifier.
    :ivar image: The URL of the comic's image.
    :ivar name: The name of the comic.
    :ivar shareable_id: The comic's shareable ID.
    :ivar url: The comic's URL.
    """

    def __init__(self, identifier: str, date: Optional[datetime] = None, *, random: bool = False) -> None:

        now = datetime.now()

        if date is not None and random:
            raise ValueError("If 'random' is 'True', 'date' must not be specified.")

        if (date is not None) and (now.year < date.year or now.month < date.month or now.day < date.day):
            raise ValueError("Date must be in the past.")

        self.identifier = identifier
        self.date = date if date else now

        if random:
            self.url = f"{GOCOMICS_BASE_URL}random/{self.identifier}"
        else:
            self.url = f"{GOCOMICS_BASE_URL}{self.identifier}/{self.date.strftime('%Y/%m/%d')}"

        page = Request(self.url)
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), 'html.parser')

        tag = soup.find("div", {"data-shareable-model": "FeatureItem"})
        self.shareable_id = int(tag.attrs["data-shareable-id"])
        self.feature_id = int(tag.attrs["data-feature-id"])
        self.name = tag.attrs["data-feature-name"]
        self.code = tag.attrs["data-feature-code"]
        self.image = tag.attrs["data-image"]
        self.creator = tag.attrs["data-creator"]
        self.formatted_date = tag.attrs["data-formatted-date"]
        self.accountable_person = tag.attrs["accountableperson"]
        self.url = tag.attrs["data-url"]

        tag = list(soup.find("div", {"class": "gc-avatar gc-avatar--creator xs"}).children)[0]
        self.avatar = tag.attrs["src"]


    @property
    def calendar(self) -> List[datetime]:
        calendar_url = f"{GOCOMICS_BASE_URL}calendar/{self.identifier}/{self.date.strftime('%Y/%m')}"
        with urlopen(calendar_url) as result:
            if result.geturl() != calendar_url:
                path = urlparse(result.geturl()).path
                calendar_url = f"{GOCOMICS_BASE_URL}calendar{path}/{self.date.strftime('%Y/%m')}"
        with urlopen(calendar_url) as result:
            calendar_list = [datetime(*[int(_element) for _element in element.replace('"', "").split("/")]) for element in load(result)]
        return calendar_list
