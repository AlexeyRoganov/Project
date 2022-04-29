from django.urls import path
# Импортируем созданное нами представление
from .views import AppointmentView


urlpatterns = [
   path('', AppointmentView.as_view(), name='make_appointment'),

]