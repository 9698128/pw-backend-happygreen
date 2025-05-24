from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),  # ← ASSICURATI CHE CI SIA
    path('api/groups/', include('apps.groups.urls')),
    path('api/posts/', include('apps.posts.urls')),
    path('api/challenges/', include('apps.challenges.urls')),
    path('api/ml-data/', include('apps.ml_data.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
