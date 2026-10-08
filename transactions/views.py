import csv

from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from users.models import AdminLog
from .filters import TransactionFilter
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')


class TransactionExportCSVView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'User', 'Card', 'Amount', 'Status', 'Description', 'Date'])

        qs = Transaction.objects.select_related('user', 'card').order_by('-created_at')
        for t in qs:
            writer.writerow([
                t.id,
                t.user.username,
                t.card.masked_number if t.card else '',
                t.amount,
                t.status,
                t.description,
                t.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])

        AdminLog.objects.create(admin=request.user, action='Exported transactions to CSV')
        return response