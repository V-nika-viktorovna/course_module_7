import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Mailing_Attempt


def change_mailing_status(mailing, current_datetime) -> None:
    """Функция проверяет статус рассылки, когда статус рассылки = "completed",
    меняет актуальность рассылки с True на False."""

    if mailing.status == "created":
        mailing.status = "launched"
        print(f"{mailing.title} launched")

    elif mailing.status == "launched":
        print(f"{mailing.title}launched")

    elif mailing.status == "launched" and mailing.datetime_finish <= current_datetime:
        mailing.status = "completed"
        mailing.is_active = False
        print(f"{mailing.title}completed")

    mailing.save()


def get_date_send(mailing, current_datetime):
    """Функция корректирует  дату и время для следующей отправки рассылки (datetime_send)."""
    if mailing.datetime_send < current_datetime:

        if mailing.periodicity == "daily":
            mailing.datetime_send += timedelta(days=1, hours=0, minutes=0)

        elif mailing.periodicity == "weekly":
            mailing.datetime_send += timedelta(days=7, hours=0, minutes=0)

        elif mailing.periodicity == "monthly":
            mailing.datetime_send += timedelta(days=30, hours=0, minutes=0)

        elif mailing.periodicity == "year":
            mailing.datetime_send += timedelta(days=365, hours=0, minutes=0)

        mailing.save()


def send_mail_one(request, pk):
    """Функция отправки запуска рассылки в любое время вне расписания.
    Отправляет письма, записывает логи с информацией об отпрвке
    Также записывает логи об ошибках в случае их возникновения."""

    t_zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(t_zone)
    mailing_data = get_object_or_404(Mailing, pk=pk)

    if mailing_data.is_active:

        change_mailing_status(mailing_data, current_datetime)

        emails = [recipient.email for recipient in mailing_data.recipient.all()]

        try:
            server_response = send_mail(subject=mailing_data.message.subject, message=mailing_data.message.body,
                                        from_email=settings.EMAIL_HOST_USER, recipient_list=emails,
                                        fail_silently=False)
            print("Письмо отправлено")
            status = "Отправлено"
            mailing_attempt = Mailing_Attempt(mailing=mailing_data, status=status,
                                              server_response=server_response, owner=mailing_data.owner)
            mailing_attempt.save()
            print("попытка рассылки сохранена")

        except smtplib.SMTPException as error:
            status = "Не отправлено"
            server_response = f"Ошибка отправки {error}"
            mailing_attempt = Mailing_Attempt(mailing=mailing_data, status=status,
                                              server_response=server_response, owner=mailing_data.owner)
            mailing_attempt.save()
            print("ошибка попытка рассылки:", error)

        finally:
            return redirect(reverse("mailing:mailing_list"))

    else:
        print("Рассылка не активна")
        return redirect(reverse("mailing:mailing_list"))


def send_mail_by_time():
    """Функция запуска всех рассылок.
    Находит все актуальные рассылки, проверяет статус каждой, отправляет письма,
    записывает логи с информацией об отпрвке
    Также записывает логи об ошибках в случае их возникновения."""

    t_zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(t_zone)

    mailing_list = Mailing.objects.all().filter(is_active=True)

    mailing_list = list(mailing_list)

    if mailing_list:
        for mailing in mailing_list:
            change_mailing_status(mailing, current_datetime)
            if mailing.datetime_send <= current_datetime <= mailing.datetime_finish:

                emails_list = [recipient.email for recipient in mailing.recipient.all()]

                try:
                    server_response = send_mail(subject=mailing.message.subject, message=mailing.message.body,
                                                from_email=settings.EMAIL_HOST_USER, recipient_list=emails_list,
                                                fail_silently=False)
                    print("Письмо отправлено")
                    status = "Отправлено"
                    mailing_attempt = Mailing_Attempt(mailing=mailing, status=status,
                                                      server_response=server_response, owner=mailing.owner)
                    mailing_attempt.save()
                    print("попытка рассылки сохранена")
                    get_date_send(mailing, current_datetime)

                    mailing_list.remove(mailing)

                except smtplib.SMTPException as error:
                    status = "Не отправлено"
                    server_response = f"Ошибка отправки {error}"
                    mailing_attempt = Mailing_Attempt(mailing=mailing, status=status,
                                                      server_response=server_response, owner=mailing.owner)
                    mailing_attempt.save()
                    print("ошибка попытка рассылки:", error)
                finally:
                    return redirect(reverse("mailing:mailing_list"))
            else:
                print("Список рассылок пуст")
                return redirect(reverse("mailing:mailing_list"))

    else:
        print("Список рассылок пуст")
        return redirect(reverse("mailing:mailing_list"))


def toggle_activity(request, pk):
    """Функция позволяет модератору сменить статус рассылки."""

    mailing_status = get_object_or_404(Mailing, pk=pk)
    if mailing_status.is_active:
        mailing_status.is_active = False

    else:
        mailing_status.is_active = True

    mailing_status.save()
    return redirect(reverse("mailing:mailing_list"))


def get_catalog_cache():
    """Функция получает данные из кэша.
     Если кэш пуст, то кэширует данные главной стпаницы"""

    if not CACHE_ENABLED:
        return Mailing.objects.all()

    products_get = cache.get("mailing_list")
    if products_get is not None:
        return products_get

    products_set = Mailing.objects.all()
    cache.set("mailing_list", products_set)
    return products_set
