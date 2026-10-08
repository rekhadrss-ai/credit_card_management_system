from django.conf import settings
from django.db import models


class Card(models.Model):
    CARD_TYPES = [('CREDIT', 'Credit'), ('DEBIT', 'Debit')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cards')
    card_holder = models.CharField(max_length=100)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    masked_number = models.CharField(max_length=19)  # ** ** ** 1234
    last4 = models.CharField(max_length=4)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.masked_number