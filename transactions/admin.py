from django.contrib import admin
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.urls import path
from django.template.response import TemplateResponse

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'description')
    change_list_template = 'admin/transactions_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom = [path('daily-summary/', self.admin_site.admin_view(self.daily_summary),
                       name='daily-summary')]
        return custom + urls

    def daily_summary(self, request):
        rows = (
            Transaction.objects
            .annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(
                total=Count('id'),
                success=Count('id', filter=__import__('django.db.models', fromlist=['Q']).Q(status='SUCCESS')),
                failed=Count('id', filter=__import__('django.db.models', fromlist=['Q']).Q(status='FAILED')),
                amount=Sum('amount', filter=__import__('django.db.models', fromlist=['Q']).Q(status='SUCCESS')),
            )
            .order_by('-day')
        )
        context = {**self.admin_site.each_context(request), 'rows': rows,
                   'title': 'Daily Payment Summary'}
        return TemplateResponse(request, 'admin/daily_summary.html', context)