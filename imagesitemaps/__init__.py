from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ImproperlyConfigured


class ImageTagException(Exception):
    pass


REQUIRED_IMAGE_TAGS = [
    "loc",
]

OPTIONAL_IMAGE_TAGS = [
    "caption",
    "geo_location",
    "title",
    "license",
]


class ImageSitemap(Sitemap):
    """
    Represents a Google image sitemap.
    """

    def image_loc(self, img):
        return img.get_absolute_url()

    def image_title(self, img):
        return img

    def images(self, obj):
        return [obj]

    def get_urls(self, page=1, site=None, protocol="http"):
        from django.contrib.sites.models import Site

        if site is None:
            try:
                site = Site.objects.get_current()
            except Site.DoesNotExist:
                pass
            if site is None:
                raise ImproperlyConfigured(
                    "In order to use Sitemaps you must either use the sites framework or "
                    "pass in a Site or RequestSite object in your view code."
                )

        urls = []
        try:
            get = self._Sitemap__get
        except AttributeError:  # Django >= 3.2
            get = self._get

        # methods with this prefix will be treated as image tags.
        ATTR_PREFIX = "image_"  # noqa

        for item in self.paginator.page(page).object_list:
            loc = "%s://%s%s" % (protocol, site.domain, get("location", item))
            image_tags = []
            for attr in dir(self):
                if attr.startswith(ATTR_PREFIX):
                    image_tags.append(attr[len(ATTR_PREFIX) :])

            url_info = {
                "location": loc,
            }

            optional_tags = image_tags[:]
            url_info["images"] = []
            for idx, img in enumerate(self.images(item)):
                url_info["images"].append({})

                # validate required tags.
                for req_tag in REQUIRED_IMAGE_TAGS:
                    if req_tag not in image_tags:
                        raise ImageTagException(
                            "<image:%s> is a required tag." % req_tag
                        )

                    url_info["images"][idx][req_tag] = get(
                        "%s%s" % (ATTR_PREFIX, req_tag), img, None
                    )
                    if req_tag in optional_tags:
                        optional_tags.remove(req_tag)

                # validate the rest of the tags
                for tag in optional_tags:
                    if tag not in OPTIONAL_IMAGE_TAGS:
                        raise ImageTagException(
                            "<image:%s> tag is not supported." % tag
                        )

                url_info["images"][idx]["optional"] = {}
                for tag in optional_tags:
                    url_info["images"][idx]["optional"][tag] = get(
                        "%s%s" % (ATTR_PREFIX, tag), img, None
                    )
            urls.append(url_info)
        return urls
