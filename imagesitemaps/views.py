from django.contrib.sites.models import Site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils.encoding import smart_str


# Unfortunately, we can't just provide custom templates for these views -
# yet this is only implemented in dev branch of Django. So we have to have
# almost copies of the original views.


def index(request, sitemaps):
    current_site = Site.objects.get_current()
    sites = []
    protocol = request.is_secure() and "https" or "http"
    for section, site in sitemaps.items():
        if callable(site):
            pages = site().paginator.num_pages
        else:
            pages = site.paginator.num_pages
        sitemap_url = reverse(
            "imagesitemaps.views.sitemap", kwargs={"section": section}
        )
        sites.append("%s://%s%s" % (protocol, current_site.domain, sitemap_url))
        if pages > 1:
            for page in range(2, pages + 1):
                sites.append(
                    "%s://%s%s?p=%s"
                    % (protocol, current_site.domain, sitemap_url, page)
                )
    xml = loader.render_to_string("sitemap_index.xml", {"sitemaps": sites})
    return HttpResponse(xml, content_type="application/xml")


def sitemap(request, sitemaps, section=None):
    maps, urls = [], []
    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps.append(sitemaps[section])
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)
    for site in maps:
        try:
            if callable(site):
                urls.extend(site().get_urls(page))
            else:
                urls.extend(site.get_urls(page))
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    xml = smart_str(loader.render_to_string("image_sitemap.xml", {"urlset": urls}))
    return HttpResponse(xml, content_type="application/xml")
