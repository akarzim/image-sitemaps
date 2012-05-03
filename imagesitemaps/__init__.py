from django.core import urlresolvers, paginator
from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site

import urllib

class ImageTagException(Exception):
    pass

REQUIRED_IMAGE_TAGS = [
    'loc',
]

OPTIONAL_IMAGE_TAGS = [
    'caption',
    'geo_location',
    'title',
    'license',
]

class ImageSitemap(Sitemap):
    """
    Represents a Google image sitemap.
    """

    def image_loc(self, obj):
        return obj.get_absolute_url()

    def image_title(self, obj):
        return unicode(obj)

    def get_urls(self, page=1, site=None):
        if site is None:
            if Site._meta.installed:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    pass
            if site is None:
                raise ImproperlyConfigured("In order to use Sitemaps you must either use the sites framework or pass in a Site or RequestSite object in your view code.")

        urls = []
        get = self._Sitemap__get

        # methods with this prefix will be treated as image tags.
        ATTR_PREFIX = 'image_'

        for item in self.paginator.page(page).object_list:
            loc = "http://%s%s" % (site.domain, get('location', item))
            image_tags = []
            for attr in dir(self):
                if attr.startswith(ATTR_PREFIX):
                    image_tags.append(attr[len(ATTR_PREFIX):])

            url_info = {
                'location':   loc,
            }

            optional_tags = image_tags[:]
            # validate required tags.
            for req_tag in REQUIRED_IMAGE_TAGS:
                if not req_tag in image_tags:
                    raise ImageTagException('<image:%s> is a required tag.' % req_tag)

                url_info[req_tag] = get('%s%s' % (ATTR_PREFIX, req_tag), item, None)
                optional_tags.remove(req_tag)

            # validate the rest of the tags
            for tag in optional_tags:
                if not tag in OPTIONAL_IMAGE_TAGS:
                    raise ImageTagException('<image:%s> tag is not supported.' % tag)

            url_info['optional'] = {}
            for tag in optional_tags:
                url_info['optional'][tag] = get('%s%s' % (ATTR_PREFIX, tag), item, None)
            urls.append(url_info)
        return urls
