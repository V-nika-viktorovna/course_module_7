from django.urls import path

from mailing.apps import MailingConfig
from mailing.services import send_mail_by_time, send_mail_one, toggle_activity
from mailing.views import (IndexView, Mailing_AttemptListView,
                           MailingCreateView, MailingDeleteView,
                           MailingDetailView, MailingListView,
                           MailingUpdateView, MessageCreateView,
                           MessageDeleteView, MessageDetailView,
                           MessageListView, MessageUpdateView,
                           RecipientCreateView, RecipientDeleteView,
                           RecipientDetailView, RecipientListView,
                           RecipientUpdateView)

app_name = MailingConfig.name

urlpatterns = [path("", IndexView.as_view(), name="index"),

               path("mailing/", MailingListView.as_view(), name="mailing_list"),

               path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_detail"),

               path("mailing/create/", MailingCreateView.as_view(), name="mailing_create"),

               path("mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),

               path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),

               path("messages/", MessageListView.as_view(), name="message_list"),

               path("messages/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),

               path("messages/create/", MessageCreateView.as_view(), name="message_create"),

               path("messages/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),

               path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),

               path("recipient/", RecipientListView.as_view(), name="recipient_list"),

               path("recipient/<int:pk>/", RecipientDetailView.as_view(), name="recipient_detail"),

               path("recipient/create/", RecipientCreateView.as_view(), name="recipient_create"),

               path("recipient/<int:pk>/update/", RecipientUpdateView.as_view(), name="recipient_update"),

               path("recipient/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),

               path("logs/", Mailing_AttemptListView.as_view(), name="logs_list"),

               path("activity/<int:pk>/", toggle_activity, name="toggle_activity"),

               path("launch/<int:pk>/", send_mail_one, name="launch_one"),

               path("launch/", send_mail_by_time, name="launch"),
               ]
