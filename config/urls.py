from typing import TYPE_CHECKING

from allauth.account.views import LoginView, LogoutView
from birdsong import urls as birdsong_urls
from coderedcms import admin_urls as crx_admin_urls
from coderedcms import search_urls as crx_search_urls
from coderedcms import urls as crx_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from wagtail.documents import urls as wagtaildocs_urls

if TYPE_CHECKING:
    from config.settings import local as LocalSettings

    settings: LocalSettings

urlpatterns = [
    # Admin, use {% url 'admin:index' %}
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
    path(settings.WAGTAIL_ADMIN_URL, include(crx_admin_urls)),
    # Documents
    path("documents/", include(wagtaildocs_urls)),
    # Search
    path("search/", include(crx_search_urls)),
    # User management
    path("users/", include("rotary_lights_website.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]

urlpatterns += [
    re_path(r"^logout/$", LogoutView.as_view(), name="account_logout"),
    re_path(r"^login/$", LoginView.as_view(), name="account_login"),
    path("mail/", include(birdsong_urls)),
    # For anything not caught by a more specific rule above, hand over to
    # the page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(crx_urls)),
]
