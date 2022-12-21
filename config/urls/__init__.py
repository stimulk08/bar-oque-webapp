from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config.settings import DEBUG


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('config.urls.api')),
    path('', include('apps.kabak.urls')),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'ui/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='ui'
        ),
    ]
