from django.urls import path
from .views import TransactionListView, TransactionExportCSVView

urlpatterns = [
    path('', TransactionListView.as_view()),
    path('export/', TransactionExportCSVView.as_view()),
]