from django.shortcuts import render
from app.service.data_provider import DataProvider
from app.service.decision import DecisionService


def index(request):
    data_provider = DataProvider()
    decision = DecisionService(data_provider)

    daily_data = data_provider.get_day_data()
    monthly_data = data_provider.get_month_data()
    predicted_data = decision.predict()

    return render(request, 'index.html', context={
        'dayData': list(map(lambda x: {'date': x.date.isoformat(), 'value': x.value}, daily_data)),
        'monthData': list(map(lambda x: {'date': x.date.isoformat(), 'value': x.value}, monthly_data)),
        'predictedData': predicted_data
    })
