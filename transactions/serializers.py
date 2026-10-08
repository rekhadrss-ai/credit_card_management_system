from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(source='card.masked_number', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'card', 'card_number', 'amount', 'status',
                  'description', 'created_at']