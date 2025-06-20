"""
MIT License

Copyright (c) 2025 Omkaar

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

from urllib.request import Request, urlopen
from typing import List, Literal, Optional, Generator
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from requests.utils import requote_uri

from .comic import Comic
from .endpoints import BASE_URL


def search(
    *,
    last_updated_today: Optional[bool] = None,
    categories: List[Literal["comicos-en-espanol", "family-comics", "funny-animals", "gag-comics", "graphic-novels", "mental-health-comics", "newspaper-comic-strips", "offbeat-comics", "office-humor", "relationship-comics", "sci-fi-fantasy-comics", "sports-comics", "vintage-comics", "webcomics", "kids"]] = None
) -> List[str]:
    """
    Returns an alphabetical list of comic identifiers.

    :param last_updated_today: If True, only return comics updated today.
    :type last_updated_today: Optional[bool]
    :param categories: A list of categories to filter the comics.
    :type categories: List[Literal["comicos-en-espanol", "family-comics", "funny-animals", "gag-comics", "graphic-novels", "mental-health-comics", "newspaper-comic-strips", "offbeat-comics", "office-humor", "relationship-comics", "sci-fi-fantasy-comics", "sports-comics", "vintage-comics", "webcomics", "kids"]]
    """
    url = f"{BASE_URL}comics/a-to-z"
    if last_updated_today and categories:
        url += f"?lastUpdated=today&category={','.join(categories)}"
    elif last_updated_today:
        url += "?lastUpdated=today"
    elif categories:
        url += f"?category={','.join(categories)}"

    page = Request(requote_uri(url))
    with urlopen(page) as result:
        soup = BeautifulSoup(result.read(), "html.parser")

    tags = soup.find_all("a", {"class": "ComicsAtoZ_comics__link__IyrQd"})
    return [tag.attrs["href"].split("/")[-1] for tag in tags if tag.attrs.get("href")]

def search_political(
    *,
    last_updated_today: Optional[bool] = None,
    categories: List[Literal["left", "center", "right"]] = None
) -> List[str]:
    """
    Returns an alphabetical list of political comic identifiers.

    :param last_updated_today: If True, only return comics updated today.
    :type last_updated_today: Optional[bool]
    :param categories: A list of political categories to filter the comics.
    :type categories: List[Literal["left", "center", "right"]]
    """
    url = f"{BASE_URL}political-cartoons/political-a-to-z"
    if last_updated_today and categories:
        url += f"?lastUpdated=today&category={','.join(categories)}"
    elif last_updated_today:
        url += "?lastUpdated=today"
    elif categories:
        url += f"?category={','.join(categories)}"

    page = Request(requote_uri(url))
    with urlopen(page) as result:
        soup = BeautifulSoup(result.read(), "html.parser")

    tags = soup.find_all("a", {"class": "ComicsAtoZ_comics__link__IyrQd"})
    return [tag.attrs["href"].split("/")[-1] for tag in tags if tag.attrs.get("href")]

def get_popular_comics(*, political: Optional[bool] = False) -> List[str]:
    """
    Returns a list of popular comic identifiers.

    :param political: If True, returns popular political comics.
    :type political: Optional[bool]
    """
    url = f"{BASE_URL}comics/popular"
    if political:
        url = f"{BASE_URL}political-cartoons/political-popular"

    page = Request(requote_uri(url))
    with urlopen(page) as result:
        soup = BeautifulSoup(result.read(), "html.parser")

    tags = soup.find_all("a", {"class": "BadgeByline_badgeByline__link__uZaRR"})
    return [tag.attrs["href"].split("/")[-1] for tag in tags if tag.attrs.get("href")]

def stream_comics(identifier: str, *, start_date: Optional[datetime] = datetime(1993, 7, 12), end_date: Optional[datetime] = datetime.today()) -> Generator[Comic]:
    """
    Streams comics for a given identifier from `start_date` to `end_date`.

    :param identifier: The comic identifier.
    :type identifier: str
    :param start_date: The start date for the comic stream.
    :type start_date: Optional[datetime]
    :param end_date: The end date for the comic stream.
    :type end_date: Optional[datetime]
    """
    current_date = start_date
    while current_date <= end_date:
        yield Comic(identifier, current_date)
        current_date += timedelta(days=1)
