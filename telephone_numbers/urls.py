from django.urls import path, register_converter

from ascertain import views
from telephone_numbers import converters

register_converter(converters.MSISDNConverter, 'msisdn')

urlpatterns = [
    path('operator/<msisdn:msisdn>/', views.WhoIsOperatorDetailView.as_view(), name='operator'),
]

