# image-sitemaps

Google image sitemaps for Django. More informations about image sitemaps on [Google Webmaster Tools](http://support.google.com/webmasters/bin/answer.py?hl=en&answer=178636&topic=20986&ctx=topic).

## Installation

You can get image-sitemaps from pypi with:

```shell
pip install image-sitemaps
```

The development version can be installed with:

```shell
pip install -e git://github.com/akarzim/image-sitemaps#egg=image-sitemaps
```

image-sitemaps introduce a new XML template therefore you should add it to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = (
    ...
    'imagesitemaps',
    ...
)
```

## Usage

Create a new file named sitemaps.py in your app directory and declare your ImageSitemap classes :
```python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
import imagesitemaps

class ImageSitemap(imagesitemaps.ImageSitemap):
    """ generic data for all ours image sitempas (use it as you used to with Django Sitemap) """  
    changefreq = 'weekly'
    priority = 0.5

    def lastmod(self, obj):
        return obj.modified

class ProductImageSitemap(ImageSitemap):
    """ a specific image sitemap for ours Product class """
    
    def items(self):
        """ Django Sitemap's items method """
        return Product.objects.all()

    def images(self, obj):
        """ this method allows you to define multiple images for an object """
        return obj.images()

    def image_loc(self, img):
        """ this required method define the image location """
        return img.doc.url

    def image_caption(self, img):
        """ this optional method define the image caption """
        return unicode(img)


    def location(self, obj):
       """ Django Sitemap's location method """
        return reverse(
            'webstore_product',
            kwargs={
                'slug_product': obj.slug,
            }
        )
```

Then you have to add this data at the end of your Django root urls.py :

```python 
from myapp.sitemaps import ProductImageSitemap

imagesitemaps = {
    'products': ProductImageSitemap,
}

urlpatterns += patterns('imagesitemaps.views',
    url(r'^sitemap-image\.xml$', 'index', {'sitemaps': imagesitemaps}),
    url(r'^sitemap-image-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': imagesitemaps}),
)
```

## Image tag definitions

<table border="1" bordercolor="#000000" cellpadding="3" cellspacing="0" width="80%">
<tbody>
  <tr>
      <td><strong>Tag</strong></td>
    <td><strong>Required</strong></td>
    <td><strong>Description</strong></td>
  </tr>
  <tr>
    <td><code>&lt;image:image&gt;</code></td>
    <td>Yes</td>
    <td>Encloses all information about a single image. Each URL (&lt;loc&gt; tag) can include up to 1,000 &lt;image:image&gt; tags.</td>
  </tr>
  <tr>
    <td><code>&lt;image:loc&gt;</code></td>
    <td>Yes</td>
    <td>The URL of the image.<p>In some cases, the image URL may not be on the same domain as your main site. This is fine, as long as both domains are verified in Webmaster Tools. If, for example, you use a content delivery network (CDN) to host your images, make sure that the hosting site is verified in Webmaster Tools OR that you submit your Sitemap using robots.txt. In addition, make sure that your robots.txt file doesn’t disallow the crawling of any content you want indexed.</p></td>
  </tr>
  <tr>
    <td><code>&lt;image:caption&gt;</code></td>
    <td>Optional</td>
    <td>The caption of the image.</td>
  </tr>
  <tr>
    <td><code>&lt;image:geo_location&gt;</code></td>
    <td>Optional</td>
    <td>The geographic location of the image. For example, <code>&lt;image:geo_location&gt;Limerick, Ireland&lt;/image:geo_location&gt;</code>.</td>
  </tr>
  <tr>
    <td><code>&lt;image:title&gt;</code></td>
    <td>Optional</td>
    <td>The title of the image.</td>
  </tr>
  <tr>
    <td><code>&lt;image:license&gt;</code></td>
    <td>Optional</td>
    <td>A URL to the license of the image.</td>
  </tr>
</tbody>
</table>


If we want to declare a new tag in our image sitemap (i.e. &lt;image:license&gt;), 
we just have to define a new method starting with `image_` in our ImageSitemap class :

```python
class ProductImageSitemap(ImageSitemap):
    ...
    def image_license(self, license):
        """ this optional method define the image license """
        return u"http://creativecommons.org/licenses/by-nd/3.0/legalcode"
```