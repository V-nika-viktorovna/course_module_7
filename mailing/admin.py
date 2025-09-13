from django.contrib import admin

from mailing.models import Mailing, Mailing_Attempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):

    list_display = ("name", "email", "owner")
    list_filter = ("name",)
    search_fields = ("email",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "owner",
        "datetime_start",
        "datetime_send",
        "datetime_finish",
        "periodicity",
        "status",
        "is_active",
    )
    list_filter = ("title",)
    search_fields = ("title", "owner")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ("id", "subject", "body", "owner")
    search_fields = ("subject", "owner")


@admin.register(Mailing_Attempt)
class Mailing_AttemptAdmin(admin.ModelAdmin):

    list_display = ("mailing", "last_time_send", "status", "server_response")
    search_fields = ("mailing",)
