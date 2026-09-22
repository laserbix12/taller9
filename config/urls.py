from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from modulo_ia.views import PredictIAView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/predict/', PredictIAView.as_view(), name='api-predict'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
