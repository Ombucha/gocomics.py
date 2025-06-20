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

from gocomics import search, search_political, get_popular_comics

class TestUtils(unittest.TestCase):
    def test_search_basic(self):
        comics = search()
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_with_last_updated_today(self):
        comics = search(last_updated_today=True)
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_with_categories(self):
        comics = search(categories=["funny-animals", "webcomics"])
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_with_last_updated_today_and_categories(self):
        comics = search(last_updated_today=True, categories=["webcomics"])
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_empty_categories(self):
        comics = search(categories=[])
        self.assertIsInstance(comics, list)

    def test_search_invalid_category(self):
        # Should not raise, but may return empty list
        comics = search(categories=["not-a-category"])
        self.assertIsInstance(comics, list)

    def test_search_political_basic(self):
        comics = search_political()
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_political_with_last_updated_today(self):
        comics = search_political(last_updated_today=True)
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_political_with_categories(self):
        comics = search_political(categories=["left", "right"])
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_political_with_last_updated_today_and_categories(self):
        comics = search_political(last_updated_today=True, categories=["center"])
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_political_empty_categories(self):
        comics = search_political(categories=[])
        self.assertIsInstance(comics, list)

    def test_search_political_invalid_category(self):
        comics = search_political(categories=["not-a-category"])
        self.assertIsInstance(comics, list)

    def test_get_popular_comics_default(self):
        comics = get_popular_comics()
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_get_popular_comics_political(self):
        comics = get_popular_comics(political=True)
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_get_popular_comics_non_political(self):
        comics = get_popular_comics(political=False)
        self.assertIsInstance(comics, list)
        self.assertTrue(all(isinstance(c, str) for c in comics))

    def test_search_return_type_and_content(self):
        comics = search()
        self.assertIsInstance(comics, list)
        for c in comics:
            self.assertIsInstance(c, str)
            self.assertTrue(len(c) > 0)

    def test_search_political_return_type_and_content(self):
        comics = search_political()
        self.assertIsInstance(comics, list)
        for c in comics:
            self.assertIsInstance(c, str)
            self.assertTrue(len(c) > 0)

    def test_get_popular_comics_return_type_and_content(self):
        comics = get_popular_comics()
        self.assertIsInstance(comics, list)
        for c in comics:
            self.assertIsInstance(c, str)
            self.assertTrue(len(c) > 0)

if __name__ == "__main__":
    unittest.main()
