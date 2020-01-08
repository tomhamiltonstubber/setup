@command
def get_commission_figures(**kwargs):
    from django.db.models import Count, Q, Sum
    from TutorCruncher.accounting.models import Invoice
    from TutorCruncher.tcsales.models import AgencyActivity
    from TutorCruncher.crm.models import Client
    from TutorCruncher.timezones import tc_now
    from dateutil.relativedelta import relativedelta

    client_ids = []
    clients = (
        Client.objects
        .filter(user__branch__agency__is_meta=True)
        .annotate(inv_count=Count('invoices', filter=Q(invoices__status=Invoice.STATUS_PAID), distinct=True))
        .filter(inv_count__lte=6, inv_count__gt=0)
    )
    for cli in clients:
        if cli.invoices.order_by('date_sent').first().date_sent >= tc_now() - relativedelta(months=6, day=1):
            client_ids.append(cli.id)
    period = (tc_now() - relativedelta(months=1)).strftime('%Y%m')
    print(f'Figures for {period}')
    print(
        AgencyActivity.objects
        .filter(agency__cligency__in=client_ids, period=int(period))
        .aggregate(v=Sum('base_fee') + Sum('revenue_usage_fee'))['v']
    )