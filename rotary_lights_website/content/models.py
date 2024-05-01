from coderedcms.models import CoderedArticleIndexPage
from coderedcms.models import CoderedArticlePage
from coderedcms.models import CoderedEventIndexPage
from coderedcms.models import CoderedEventOccurrence
from coderedcms.models import CoderedEventPage
from coderedcms.models import CoderedWebPage
from modelcluster.fields import ParentalKey


class RotaryWebPage(CoderedWebPage):
    """General purpose page with featureful streamfield and SEO attrs."""

    class Meta:
        verbose_name = "Web Page"
        verbose_name_plural = "Web Pages"

    template = "coderedcms/pages/web_page.html"


class RotaryArticleIndexPage(CoderedArticleIndexPage):
    """Index page for a series of events."""

    class Meta:
        verbose_name = "Article Index Page"
        verbose_name_plural = "Article Index Pages"

    index_query_pagemodel = "content.RotaryArticlePage"
    subpage_types = ["content.RotaryArticlePage"]
    template = "coderedcms/pages/article_index_page.html"


class RotaryArticlePage(CoderedArticlePage):
    class Meta:
        verbose_name = "Article Page"
        verbose_name_plural = "Article Pages"

    parent_page_types = ["content.RotaryArticleIndexPage"]
    subpage_types = []
    template = "coderedcms/pages/article_page.html"


class RotaryEventIndexPage(CoderedEventIndexPage):
    """Index page for a series of events."""

    class Meta:
        verbose_name = "Event Index Page"
        verbose_name_plural = "Event Index Pages"

    index_query_pagemodel = "content.RotaryEventPage"
    subpage_types = ["content.RotaryEventPage"]
    template = "coderedcms/pages/event_index_page.html"


class RotaryEventPage(CoderedEventPage):
    """An event hosted, sponsored, or supported by the Rotary Lights Org."""

    class Meta:
        verbose_name = "Event Page"
        verbose_name_plural = "Event Pages"

    parent_page_types = ["content.RotaryEventIndexPage"]
    subpage_types = []
    template = "coderedcms/pages/event_page.html"


class RotaryEventOccurrence(CoderedEventOccurrence):
    event = ParentalKey(RotaryEventPage, related_name="occurrences")
