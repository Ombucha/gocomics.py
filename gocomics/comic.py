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

from datetime import datetime
from re import search
from functools import cached_property
from urllib.parse import urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from typing import List, Optional
from json import loads
from subprocess import run
from platform import system

from bs4 import BeautifulSoup
from requests.utils import requote_uri

from .endpoints import BASE_URL

RETRY_COUNT = 10


class Comic:

    """
    A class that represents a comic.

    .. note::

        The latest comic is shown if no date is provided.
        Random comics are not supported because a comic is not released every day.

    .. note::

        Update the value of `RETRY_COUNT` if you encounter issues with fetching comic data.

    :param identifier: The comic's identifier.
    :type identifier: :class:`str`
    :param date: The comic's date.
    :type date: Optional[:class:`datetime`]
    :ivar url: The URL of the comic.
    :ivar title: The title of the comic.
    :ivar description: The description of the comic.
    :ivar share_image_url: The URL of the comic's share image.
    :ivar keywords: The keywords associated with the comic.
    :ivar author: The author of the comic.
    :ivar followers_count: The number of followers of the comic.
    :ivar name: The name of the comic.
    :ivar header_feature_url: The URL of the comic's header feature image.
    :ivar image_url: The URL of the comic's main image.
    :ivar about: A list of hyperlinks and text describing the comic.
    :ivar about_feature_url: The URL of the comic's about feature image.
    :ivar about_author: A list of hyperlinks and text describing the comic's author.
    :ivar author_image_url: The URL of the comic author's image.
    :ivar social_urls: A list of hyperlinks to the comic's social media profiles.
    :ivar characters: A list of characters in the comic.
    """

    class Hyperlink:
        """
        A class that represents a hyperlink.

        :param url: The URL of the hyperlink.
        :type url: :class:`str`
        :param text: The text of the hyperlink.
        :type text: :class:`str`
        """
        def __init__(self, url: str, text: str) -> None:
            self.url = url
            self.text = text

        def __str__(self) -> str:
            return self.text

        def __repr__(self) -> str:
            return f"Hyperlink(url={self.url}, text={self.text})"

    class Character:
        """
        A class that represents a character in a comic.

        :param name: The name of the character.
        :type name: :class:`str`
        :param image_url: The URL of the character's image.
        :type image_url: :class:`str`
        :param description: A description of the character.
        :type description: :class:`str`
        """
        def __init__(self, name: str, image_url: str, description: str) -> None:
            self.name = name
            self.image_url = image_url
            self.description = description

    def __init__(self, identifier: str, date: Optional[datetime] = None) -> None:

        if date and (date.year > datetime.today().year or date.month > datetime.today().month or date.day > datetime.today().day):
            raise ValueError("Date cannot be in the future.")

        self.identifier = identifier
        self.date = date

        if date is None:
            self.url = f"{BASE_URL}{self.identifier}"
        else:
            self.url = f"{BASE_URL}{self.identifier}/{self.date.strftime('%Y/%m/%d')}"

        try:
            page = Request(self.url)
            with urlopen(page) as result:
                soup = BeautifulSoup(result.read(), "html.parser")
        except HTTPError as e:
            raise ValueError(f"Comic with identifier '{identifier}' and date '{date}' does not exist.") from e
        except Exception as e:
            raise ValueError("An error occurred while fetching the comic.") from e

        tag = soup.find("meta", {"property": "og:title"})
        self.title = tag.attrs["content"] if tag else None

        tag = soup.find("meta", {"property": "og:description"})
        self.description = tag.attrs["content"] if tag else None

        tag = soup.find("meta", {"property": "og:image"})
        self.share_image_url = tag.attrs["content"] if tag else None

        tag = soup.find("meta", {"name": "keywords"})
        self.keywords = tag.attrs["content"].split(", ") if tag else None

        tag = soup.find("span", {"class": "Typography_typography__C_Hp6 Typography_typography_body2___WsK9"}).text.split(" | ")
        self.author = tag[0][3:] if tag else None
        self.followers_count = tag[1].split(" ")[0] if tag else None

        tag = soup.find("h1", {"class": "Typography_typography__C_Hp6 Typography_typography_d2__3FxkY"})
        self.name = tag.text if tag else None

        tag = soup.find("div", {"class": "HeaderFeature_headerFeature__backgroundImage__ipPVn"})
        style = tag.attrs["style"] if tag else None
        if style:
            match = search(r'url\("([^"]+)"\)', style)
            self.header_feature_url = urlunparse(urlparse(match.group(1))._replace(query="")) if match else None

        for _ in range(RETRY_COUNT):
            tag = soup.find("div", {"id": "S:4"})
            if tag:
                subtag = tag.find("script", {"type": "application/ld+json"})
                if subtag:
                    self.image_url = loads(subtag.text)["contentUrl"]
                    break

    def __eq__(self, __o: Comic) -> bool:
        if not isinstance(__o, Comic):
            return False
        return self.url == __o.url

    @cached_property
    def about(self) -> List[Hyperlink | str]:
        page = Request(requote_uri(f"{BASE_URL}{self.identifier}/about"))
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        tags = soup.find("div", {"class": "AboutFeature_aboutFeature__details__ru_As"}).find("div", {"class": "RichTextParser_richTextParser__joxf7"}).find_all("p")
        subtags = []
        for tag in tags:
            subtags.extend(list(tag.descendants))

        text = []
        index = 0
        while index < len(subtags):
            if subtags[index].name == "a":
                text.append(self.Hyperlink(subtags[index].attrs["href"], subtags[index].text))
                index += 2
            else:
                text.append(subtags[index].text)
                index += 1
        return text

    @cached_property
    def about_feature_url(self) -> str:
        page = Request(requote_uri(f"{BASE_URL}{self.identifier}/about"))
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        tag = soup.find("div", {"class": "AboutFeature_aboutFeature__imageContainer__nE23W"}).find("img")
        urls = tag.attrs["srcset"].split(", ") if tag else []

        banner_url = urls[0].split(" ")[0] if urls else None
        if banner_url:
            return urlunparse(urlparse(banner_url)._replace(query=""))
        return None

    @cached_property
    def about_author(self) -> List[Hyperlink | str]:
        page = Request(requote_uri(f"{BASE_URL}{self.identifier}/about"))
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        tags = soup.find("div", {"class": "AboutCreator_aboutCreator__details__6YZp3"}).find("div", {"class": "RichTextParser_richTextParser__joxf7"}).find_all("p")
        subtags = []
        for tag in tags:
            subtags.extend(list(tag.descendants))

        text = []
        index = 0
        while index < len(subtags):
            if subtags[index].name == "a":
                text.append(self.Hyperlink(subtags[index].attrs["href"], subtags[index].text))
                index += 2
            else:
                text.append(subtags[index].text)
                index += 1
        return text

    @cached_property
    def author_image_url(self) -> str:
        page = Request(requote_uri(f"{BASE_URL}{self.identifier}/about"))
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        tag = soup.find("div", {"class": "AboutCreator_aboutCreator__tcSD7"}).find("img")
        urls = tag.attrs["srcset"].split(", ") if tag else []

        image_url = urls[0].split(" ")[0] if urls else None
        if image_url:
            return urlunparse(urlparse(image_url)._replace(query=""))
        return None

    @cached_property
    def social_urls(self) -> List[Hyperlink]:
        page = Request(requote_uri(f"{BASE_URL}{self.identifier}/about"))
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        tags = soup.find_all("a", {"class": "SocialLinks_socialLinks__link__84fhl"})
        return [tag.attrs["href"] for tag in tags]

    @cached_property
    def characters(self) -> List[Character]:
        page = Request(requote_uri(f"{BASE_URL}{self.identifier}/about"))
        with urlopen(page) as result:
            soup = BeautifulSoup(result.read(), "html.parser")

        tags = soup.find_all("div", {"class": "AboutCharacter_aboutCharacter__cAOuK"})
        characters = []
        for tag in tags:
            name = tag.find("h3").text if tag.find("h3") else None
            image_tag = tag.find("img")
            image_url = image_tag.attrs["srcset"].split(", ")[0].split(" ")[0] if image_tag else None
            description = tag.find("p").text if tag.find("p") else None

            if name and image_url and description:
                characters.append(self.Character(name, urlunparse(urlparse(image_url)._replace(query="")), description))
        return characters

    def download(self, *, filename: Optional[str] = None, path: Optional[str] = None) -> str:
        """
        Downloads the comic image and returns the file path.

        :param filename: Optional filename for the downloaded image.
        :type filename: Optional[str]
        :param path: Optional path where the image will be saved.
        :type path: Optional[str]
        """
        if not self.image_url:
            raise ValueError("Comic does not have an image URL.")

        if filename is None:
            filename = f"{self.identifier}.png"

        if path is None:
            path = "."

        if filename.split(".")[-1] not in ["png", "jpg", "jpeg"]:
            raise ValueError("Filename must end with .png, .jpg, or .jpeg")

        full_path = f"{path}/{filename}"
        req = Request(requote_uri(self.image_url))

        with urlopen(req) as response, open(full_path, "wb") as out_file:
            out_file.write(response.read())

        return full_path

    def refresh(self) -> None:
        """
        Refreshes the comic data by re-fetching it from the website. It can be useful if a particular attribute is not set or if you want to update the comic's data without creating a new instance.
        """
        self.__init__(self.identifier, self.date)

    def show(self, *, filename: Optional[str] = None, path: Optional[str] = None) -> None:
        """
        Opens the comic's URL in the default image viewer app.

        :param filename: Optional filename for the downloaded image.
        :type filename: Optional[str]
        :param path: Optional path where the image will be saved.
        :type path: Optional[str]
        """
        run(['open' if system() == 'Darwin' else 'xdg-open' if system() == 'Linux' else 'start', self.download(filename=filename, path=path)], shell=True, check=False)
