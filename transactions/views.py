import csv

from rest_framework.response import Response
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import generics, serializers
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

class PaymentDocSerializer(serializers.Serializer):
    card_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(required=False)


class PaymentDocView(APIView):
    """Documentation only. The real payment runs on FastAPI at http://127.0.0.1:8001/api/payments/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(request=PaymentDocSerializer, tags=['payments'],
                   summary='Make payment (served by FastAPI on port 8001)')
    def post(self, request):
        return Response({'detail': 'Send this request to http://127.0.0.1:8001/api/payments/'},
                        status=400)