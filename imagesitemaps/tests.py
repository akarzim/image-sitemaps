"""
Test Google Image Sitemaps
"""

from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django.urls import path, reverse

from imagesitemaps import ImageSitemap, views


class TestSitemapObject(object):
    def get_absolute_url(self):
        return "foo"


TEST_IMAGE_TAGS = ("loc", "title", "caption", "license")

# fixture
TEST_VALUES = (
    (
        "/html-5/thumb.jpg",
        "HTML5",
        "HTML 5",
        "http://creativecommons.org/licenses/by-nd/3.0/legalcode",
    ),
    (
        "/cars/honda-5d/thumb.jpg",
        "Honda 5D",
        "5 doors Honda",
        "http://creativecommons.org/licenses/by-nd/3.0/legalcode",
    ),
    (
        "/my-apple/thumb.jpg",
        "Golden apple",
        "Completely golden",
        "http://creativecommons.org/licenses/by-nd/3.0/legalcode",
    ),
)


def get_test_objects():
    for val in TEST_VALUES:
        obj = TestSitemapObject()
        setattr(obj, "location", val[0])
        # val = val[1:]
        for i, tag in enumerate(TEST_IMAGE_TAGS):
            setattr(obj, tag, val[i])
        yield obj


class TestImageSitemap(ImageSitemap):
    def items(self):
        return [i for i in get_test_objects()]

    def location(self, obj):
        return obj.location

    def image_title(self, img):
        return img.title

    def image_caption(self, img):
        return img.caption


image_sitemaps = {
    "": TestImageSitemap,
}


class ImageSitemapTest(TestCase):
    def setUp(self):
        self.urlconf = import_module(settings.ROOT_URLCONF)
        self.original_urlpatterns = self.urlconf.urlpatterns[:]
        self.urlconf.urlpatterns += [
            path(
                "image_sitemap.xml",
                views.sitemap,
                {"sitemaps": image_sitemaps},
                name="test_image_sitemap",
            ),
        ]
        self.sitemap_view = reverse("test_image_sitemap")
        self.test_objects = [i for i in get_test_objects()]

    @override_settings(SITE_ID=2)
    def test_no_site_error(self):
        with self.assertRaisesRegex(
            ImproperlyConfigured,
            "^In order to use Sitemaps you must either use the sites framework or "
            "pass in a Site or RequestSite object in your view code.$",
        ):
            ImageSitemap().get_urls()

    def get_document(self):
        from xml.dom.minidom import parseString

        response = self.client.get(self.sitemap_view)
        return parseString(response.content)

    def test_valid_xml(self):
        """
        Test if the sitemap is a valid XML document.
        """
        self.get_document()

    def test_valid_sitemap_dom(self):
        doc = self.get_document()
        self.assertEqual(doc.documentElement.nodeName, "urlset")
        urlset = doc.documentElement
        # xlmns test
        self.assertTrue(urlset.hasAttribute("xmlns:image"))
        self.assertTrue(urlset.hasAttribute("xmlns"))
        urls = urlset.getElementsByTagName("url")
        self.assertEqual(len(urls), len(self.test_objects))
        result_xml = []
        for url in urls:
            locs = url.getElementsByTagName("loc")
            self.assertTrue(len(locs), 1)
            images = url.getElementsByTagName("image:image")
            self.assertTrue(len(images), 1)
            image = images[0]
            result_xml.append(image.toprettyxml())
        self.assertEqual(len(result_xml), 3)
        self.assertEqual(
            result_xml[0],
            "<image:image>\n\t<image:loc>foo</image:loc>\n\t<image:caption>HTML 5</image:caption>"
            "\n\t<image:title>HTML5</image:title>\n</image:image>\n",
        )
        self.assertEqual(
            result_xml[1],
            "<image:image>\n\t<image:loc>foo</image:loc>\n\t<image:caption>5 doors Honda</image:caption>"
            "\n\t<image:title>Honda 5D</image:title>\n</image:image>\n",
        )
        self.assertEqual(
            result_xml[2],
            "<image:image>\n\t<image:loc>foo</image:loc>\n\t<image:caption>Completely golden</image:caption>"
            "\n\t<image:title>Golden apple</image:title>\n</image:image>\n",
        )

    def tearDown(self):
        self.urlconf.urlpatterns = self.original_urlpatterns
