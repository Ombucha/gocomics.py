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


# pylint: skip-file

import unittest

from datetime import datetime, timedelta
from gocomics import Comic

class TestComic(unittest.TestCase):
    def setUp(self):
        self.identifier = "calvinandhobbes"
        self.today = datetime.now()
        self.past_date = self.today - timedelta(days=10)

    def test_comic_init_valid(self):
        comic = Comic(self.identifier)
        self.assertEqual(comic.identifier, self.identifier)
        self.assertIsNone(comic.date)
        self.assertTrue(comic.url.endswith(self.identifier))

    def test_comic_init_with_date(self):
        comic = Comic(self.identifier, self.past_date)
        self.assertEqual(comic.identifier, self.identifier)
        self.assertEqual(comic.date, self.past_date)
        self.assertIn(self.past_date.strftime('%Y/%m/%d'), comic.url)

    def test_comic_init_future_date(self):
        future = self.today + timedelta(days=10)
        with self.assertRaises(ValueError):
            Comic(self.identifier, future)

    def test_comic_init_invalid_identifier(self):
        with self.assertRaises(ValueError):
            Comic("notarealcomic1234567890")

    def test_comic_equality(self):
        comic1 = Comic(self.identifier)
        comic2 = Comic(self.identifier)
        self.assertEqual(comic1, comic2)
        comic3 = Comic("garfield")
        self.assertNotEqual(comic1, comic3)
        self.assertNotEqual(comic1, "notacomictype")

    def test_hyperlink_repr_and_str(self):
        h = Comic.Hyperlink("https://example.com", "Example")
        self.assertEqual(str(h), "Example")
        self.assertIn("Example", repr(h))
        self.assertIn("https://example.com", repr(h))

    def test_character_init_and_str(self):
        c = Comic.Character("Name", "https://img", "desc")
        self.assertEqual(c.name, "Name")
        self.assertEqual(c.image_url, "https://img")
        self.assertEqual(c.description, "desc")
        self.assertIsInstance(str(c), str)
        self.assertIsInstance(repr(c), str)

    def test_about_property(self):
        comic = Comic(self.identifier)
        about = comic.about
        self.assertIsInstance(about, list)
        for item in about:
            self.assertTrue(isinstance(item, str) or isinstance(item, Comic.Hyperlink))

    def test_about_feature_url(self):
        comic = Comic(self.identifier)
        url = comic.about_feature_url
        self.assertTrue(url is None or isinstance(url, str))

    def test_about_author(self):
        comic = Comic(self.identifier)
        about_author = comic.about_author
        self.assertIsInstance(about_author, list)
        for item in about_author:
            self.assertTrue(isinstance(item, str) or isinstance(item, Comic.Hyperlink))

    def test_author_image_url(self):
        comic = Comic(self.identifier)
        url = comic.author_image_url
        self.assertTrue(url is None or isinstance(url, str))

    def test_social_urls(self):
        comic = Comic(self.identifier)
        urls = comic.social_urls
        self.assertIsInstance(urls, list)
        for url in urls:
            self.assertIsInstance(url, str)

    def test_characters(self):
        comic = Comic(self.identifier)
        chars = comic.characters
        self.assertIsInstance(chars, list)
        for char in chars:
            self.assertIsInstance(char, Comic.Character)
            self.assertIsInstance(char.name, str)
            self.assertIsInstance(char.image_url, str)
            self.assertIsInstance(char.description, str)

    def test_properties_types(self):
        comic = Comic(self.identifier)
        self.assertIsInstance(comic.title, (str, type(None)))
        self.assertIsInstance(comic.description, (str, type(None)))
        self.assertIsInstance(comic.share_image_url, (str, type(None)))
        self.assertIsInstance(comic.keywords, (list, type(None)))
        self.assertIsInstance(comic.author, (str, type(None)))
        self.assertIsInstance(comic.followers_count, (str, type(None)))
        self.assertIsInstance(comic.name, (str, type(None)))
        self.assertIsInstance(comic.header_feature_url, (str, type(None)))
        self.assertIsInstance(comic.image_url, (str, type(None)))

if __name__ == "__main__":
    unittest.main()
