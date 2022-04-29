from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import mail_admins
from datetime import datetime
from django.template.loader import render_to_string
from .models import Appointment
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers


# def notify_managers_appointment(sender, instance, created, **kwargs):
#     subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
#
#     if created:
#         subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
#     else:
#         subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'
#
#     mail_managers(
#         subject=subject,
#         message=instance.message,
#     )
#
#
# # коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
# post_save.connect(notify_managers_appointment, sender=Appointment)


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('appointments:make_appointment')
