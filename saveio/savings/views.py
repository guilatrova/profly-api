from datetime import date

from django.http import HttpResponse

from .services import TransactionsCSVDataFactory

data_factory = TransactionsCSVDataFactory()


def get_csv_name():
    suffix = str(date.today())
    return f"profly_transactions_{suffix}.csv"


def transactions_as_csv_view(request):
    csv_name = get_csv_name()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{csv_name}"'

    data_factory.write_data(response)

    return response
