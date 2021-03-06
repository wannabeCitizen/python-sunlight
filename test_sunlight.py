try:
    import unittest2 as unittest
except ImportError:
    import unittest

import sunlight


class TestCongress(unittest.TestCase):

    def test_get(self):
        resp = sunlight.congress.get([''])
        self.assertIsNotNone(resp)

    def test__get_url(self):
        url = sunlight.congress._get_url(['bills'],
                                         sunlight.config.API_KEY)

        expected_url = "{base_url}/bills?apikey={apikey}".format(
            base_url='https://congress.api.sunlightfoundation.com',
            apikey=sunlight.config.API_KEY)

        self.assertEqual(url, expected_url)

    def test_pathlist__get_url(self):
        url = sunlight.congress._get_url(['legislators', 'locate'],
                                         sunlight.config.API_KEY)

        expected_url = "{base_url}/legislators/locate?apikey={apikey}".format(
            base_url='https://congress.api.sunlightfoundation.com',
            apikey=sunlight.config.API_KEY)

        self.assertEqual(url, expected_url)

    def test_legislators(self):
        results = sunlight.congress.legislators()
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_search_bills(self):
        results = sunlight.congress.search_bills('Affordable Care Act')
        page = results._meta.get('page', None)
        self.assertIsNotNone(page)
        if page:
            self.assertEqual(page.get('page', None), 1)
            self.assertEqual(page.get('count', None), 20)
        self.assertNotEqual(len(results), 0)

    def test_locate_districts_by_zip(self):
        results = sunlight.congress.locate_districts_by_zip(27514)
        count = results._meta.get('count', None)
        self.assertNotEqual(len(results), 0)
        self.assertEqual(len(results), count)


class TestCapitolWords(unittest.TestCase):

    def setUp(self):
        self.phrases_kwargs = {
            'entity_type': 'legislator',
            'entity_value':  'L000551'
        }

    def test__get_url(self):
        url = sunlight.capitolwords._get_url(['phrases'],
                                             sunlight.config.API_KEY,
                                             **self.phrases_kwargs)

        expected_url = '{base_url}/phrases.json?apikey={apikey}&{args}'.format(
            base_url='http://capitolwords.org/api/1',
            apikey=sunlight.config.API_KEY,
            args=sunlight.service.safe_encode(self.phrases_kwargs)).strip('&')

        self.assertEqual(url, expected_url)

    def test_dates(self):
        results = sunlight.capitolwords.dates('Obamacare')
        self.assertNotEqual(len(results), 0)

    def test_phrases_by_entity(self):
        results = sunlight.capitolwords.phrases_by_entity('state', phrase='Obamacare')
        self.assertNotEqual(len(results), 0)

    def test_legislator_phrases(self):
        results = sunlight.capitolwords.phrases(
            self.phrases_kwargs['entity_type'],
            self.phrases_kwargs['entity_value'])

        self.assertNotEqual(len(results), 0)

    def test_text(self):
        results = sunlight.capitolwords.text('Christmas')
        self.assertNotEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
