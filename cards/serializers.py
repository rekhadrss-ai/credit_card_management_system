from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    card_number = serializers.CharField(write_only=True)

    class Meta:
        model = Card
        fields = ['id', 'card_holder', 'card_type', 'card_number',
                  'masked_number', 'last4', 'expiry_month',
                  'expiry_year', 'created_at']
        read_only_fields = ['id', 'masked_number', 'last4', 'created_at']

    def validate_card_number(self, value):
        value = value.replace(' ', '')
        if not value.isdigit() or not (13 <= len(value) <= 19):
            raise serializers.ValidationError('Card number must be 13 to 19 digits.')
        return value

    def validate_expiry_month(self, value):
        if not 1 <= value <= 12:
            raise serializers.ValidationError('Month must be between 1 and 12.')
        return value

    def validate(self, attrs):
        if 'cvv' in self.initial_data:
            raise serializers.ValidationError({'cvv': 'CVV must never be sent or stored.'})
        return attrs

    def create(self, validated_data):
        number = validated_data.pop('card_number')  # removed, never saved
        last4 = number[-4:]
        validated_data['last4'] = last4
        validated_data['masked_number'] = '**** **** **** ' + last4
        return Card.objects.create(**validated_data)