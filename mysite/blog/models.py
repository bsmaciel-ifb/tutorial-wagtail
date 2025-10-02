from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context['blogpages'] = blogpages
        return context

    content_panels = Page.content_panels + ["intro"]

class BlogPostPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        "date", "intro", "body", "gallery_images"
        ]

class BlogPostPageGalleryImage(Orderable):
    page = ParentalKey(BlogPostPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]