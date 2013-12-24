from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = patterns("",
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    #scorecard include home too
    url(r"^$", include("scorecard.urls")),
    url(r"^scorecard/", include("scorecard.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
