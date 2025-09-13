from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, Mailing_Attempt, Message, Recipient
from mailing.services import get_catalog_cache


class MailingListView(ListView):

    model = Mailing
    template_name = 'mailing_list.html'


class MailingDetailView(LoginRequiredMixin, DetailView):

    model = Mailing
    template_name = "mailing_detail.html"


class MailingCreateView(LoginRequiredMixin, CreateView):

    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):

        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):

    model = Mailing
    template_name = "mailing_form.html"
    form_class = MailingForm
    success_url = reverse_lazy("mailing:mailing_list")

    def get_form_class(self):
        """Метод выводит пользователю форму для редактирования,
        в зависимости от прав доступа пользователя."""
        user = self.request.user
        if user == self.object.owner or self.request.user.is_superuser:
            return MailingForm

        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):

    model = Mailing
    template_name = "mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


class MessageListView(ListView):

    model = Message
    template_name = "message_list.html"


class MessageDetailView(LoginRequiredMixin, DetailView):

    model = Message
    template_name = "message_detail.html"


class MessageCreateView(LoginRequiredMixin, CreateView):

    model = Message
    form_class = MessageForm
    template_name = "message_form.html"

    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form):

        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):

    model = Message
    form_class = MessageForm
    template_name = "message_form.html"
    success_url = reverse_lazy("mailing:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):

    model = Message
    template_name = "message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


class RecipientListView(ListView):

    model = Recipient
    template_name = "recipient_list.html"


class RecipientDetailView(LoginRequiredMixin, DetailView):

    model = Recipient
    template_name = "recipient_detail.html"


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_form.html"

    success_url = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form):

        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")


class IndexView(TemplateView):

    template_name = "index.html"

    def get_queryset(self):
        return get_catalog_cache()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        mailing_count = Mailing.objects.all()
        if mailing_count is None:
            context["mailing_count"] = "Сообщений нет"
        else:
            mailing_count = mailing_count.count()
            context["mailing_count"] = mailing_count

        unique_recipient_count = Recipient.objects.all().values("email").distinct()
        if unique_recipient_count is None:
            context["unique_recipient_count"] = "Получателей нет"
        else:
            unique_recipient_count = unique_recipient_count.count()
            context["unique_recipient_count"] = unique_recipient_count

        active_mailing_count = Mailing.objects.filter(is_active=True)
        if active_mailing_count is None:
            context["active_mailing_count"] = "Активных сообщений нет"
        else:
            active_mailing_count = active_mailing_count.count()
            context["active_mailing_count"] = active_mailing_count

        return context


class Mailing_AttemptListView(ListView):
    model = Mailing_Attempt
    template_name = "log_list.html"

    def get_queryset(self, *args, **kwargs):
        """Метод вывода логов, только для автора рассылок,
        при отправке которых эти логи сформированы."""
        user = self.request.user
        if user.is_staff:
            queryset = super().get_queryset(*args, **kwargs)
        elif user.is_superuser:
            queryset = super().get_queryset(*args, **kwargs)
        else:
            queryset = super().get_queryset().filter(owner=user)
        return queryset
