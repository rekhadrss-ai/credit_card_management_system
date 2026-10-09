from django.urls import path
from .views import TransactionListView, TransactionExportCSVView, PaymentDocView


urlpatterns = [
    path('', TransactionListView.as_view()),
    path('export/', TransactionExportCSVView.as_view()),
    path('payment-docs/', PaymentDocView.as_view()),
]