from django.urls import resolve
from django.test import TestCase
from HoundSploit.views import home_page


class TestPageTest(TestCase):

    def test_root_url_resolves_to_search_page_view(self):
        found = resolve('/search')
        self.assertEqual(found.func, home_page)

