from django.db import models
from django.utils import timezone

from users.models import User

NULFLAG = {"blank": True, "null": True}


class Recipient(models.Model):
    """Модель получателя рассылки"""

    email = models.EmailField(verbose_name="Электронная почта", help_text="Электронная почта")

    name = models.CharField(max_length=200, verbose_name="ФИО", help_text="ФИО")

    comment = models.TextField(verbose_name="Комментарий", help_text="Комментарий", **NULFLAG)

    owner = models.ForeignKey(User, verbose_name="Владелец", on_delete=models.CASCADE, **NULFLAG)

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"

    def __str__(self):
        return f"Получатель рассылки: {self.name}"


class Message(models.Model):
    """Модели сообщение"""

    subject = models.CharField(max_length=240, verbose_name="Тема письма", help_text="Тема письма",  **NULFLAG)

    body = models.TextField(verbose_name="Тело письма", help_text="Заполните тело сообщения",  **NULFLAG)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", help_text="Владелец",
                              **NULFLAG)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("set_update", "Может менять сообщения"),
        ]

    def __str__(self):
        return f"Тема письма: {self.subject}. содержание: {self.body}"


class Mailing(models.Model):
    """Модели рассылка"""

    PERIOD_CHOICES = [
        ("day", "раз в день"),
        ("week", "раз в неделю"),
        ("month", "раз в месяц"),
        ("year", "раз в год"),
    ]

    STATUS_CHOICES = [
        ("completed", "Завершена"),
        ("created", "Создана"),
        ("launched", "Запущена"),
    ]

    title = models.CharField(max_length=200, verbose_name=" Название рассылки", help_text="Напишите название рассылки")

    owner = models.ForeignKey(User, verbose_name="Владелец рассылки", on_delete=models.CASCADE, **NULFLAG)

    message = models.ForeignKey(Message, verbose_name="Сообщение рассылки", on_delete=models.CASCADE)

    datetime_start = models.DateTimeField(default=timezone.now, verbose_name="Дата начала рассылки",
                                          help_text="Дата начала рассылки")

    datetime_send = models.DateTimeField(default=timezone.now, verbose_name="Дата отправки",
                                         help_text="Дата отправки")

    datetime_finish = models.DateTimeField(default=timezone.now, verbose_name="Дата окончания рассылки",
                                           help_text="Дата окончания рассылки")

    periodicity = models.CharField(max_length=20, choices=PERIOD_CHOICES, default="year",
                                   verbose_name="Периодичность", help_text="Периодичность")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created", verbose_name="Статус рассылки",
                              help_text="Статус рассылки")

    recipient = models.ManyToManyField(Recipient, verbose_name="Получатели рассылки", help_text="Получатели рассылки")

    is_active = models.BooleanField(default=True, verbose_name="Активность", help_text="Активность")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("set_is_active", "Может менять активность рассылки"),
            ("launching_mailing", "Может запускать рассылки"),
        ]

    def __str__(self):
        return f"Рассылка {self.title}"


class Mailing_Attempt(models.Model):
    """Модель попытки рассылки"""

    mailing = models.ForeignKey(Mailing, verbose_name="Рассылка", help_text="Рассылка", on_delete=models.CASCADE)

    last_time_send = models.DateTimeField(auto_now=True, verbose_name="Дата и время последней попытки",
                                          help_text="Дата и время последней попытки")

    status = models.CharField(max_length=50, verbose_name="Статус попытки", help_text="Статус попытки")

    server_response = models.TextField(verbose_name="Ответ сервера", help_text="Ответ сервера", **NULFLAG)

    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Владелец", on_delete=models.CASCADE, **NULFLAG)

    class Meta:
        verbose_name = "Попыткиа рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"{self.mailing}. Дата и время последней попытки:{self.last_time_send}, статус попытки:{self.status}"
