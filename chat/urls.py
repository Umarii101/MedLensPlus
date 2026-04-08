from django.urls import path
from .views import ChatAPIView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('chat/', ChatAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
