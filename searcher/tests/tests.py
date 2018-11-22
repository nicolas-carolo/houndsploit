from django.test import TestCase


class TestPageTest(TestCase):

    def test_root_url_resolves_to_search_page_view(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

