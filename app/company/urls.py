from django.urls import path

from .views import (
    about_view,
    contacts_view,
    send_message_view,
    become_dealer_view,
)

urlpatterns = [
    path('about/', about_view, name='about'),
    path('contacts', contacts_view, name='contacts'),
    path('message/', send_message_view, name='send_message'),
    path('dealer/', become_dealer_view, name='become_dealer'),
]
