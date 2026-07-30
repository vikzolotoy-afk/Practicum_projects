import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve

from api.views import redirect_short_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('s/<int:id>/', redirect_short_url, name='short_url'),
    path('api/', include('api.urls')),
    path(
        'openapi-schema.yml',
        serve,
        {
            'document_root': os.path.join(settings.BASE_DIR.parent, 'docs'),
            'path': 'openapi-schema.yml',
        },
    ),
    path(
        '', TemplateView.as_view(template_name='redoc.html'), name='redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
