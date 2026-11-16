from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("chat/", views.chat, name="chat"),
    path(
    "chat-history/<int:document_id>/",
    views.chat_history,
    name="chat_history"
    ),
]