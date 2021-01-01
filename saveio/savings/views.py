from django.http import HttpResponse

from .services import TransactionsCSVDataFactory


def transactions_as_csv_view(request):
    response = HttpResponse(content_type="text/csv")

    data_factory = TransactionsCSVDataFactory(response)
    data_factory.write_data()

    return response
