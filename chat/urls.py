from django.urls import path
from .views import ChatAPIView, ChatDetailAPIView, ChatListAPIView, RegisterAPIView, LoginAPIView
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path("chat/", ChatAPIView.as_view()),
    path("chat/<int:chat_id>/", ChatDetailAPIView.as_view()),
    path("chats/", ChatListAPIView.as_view()),
    path("register/", RegisterAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
