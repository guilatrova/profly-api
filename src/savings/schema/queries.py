import graphene
from graphene_django import DjangoListField
from graphene_django.filter import DjangoFilterConnectionField

from currencies.services import CurrencyRateService
from markets.factories import ChartDataFactory
from markets.services import StocksMarketService
from savings.models import Stock, StockTransaction

from . import types

currency_service = CurrencyRateService()
market_service = StocksMarketService()
data_factory = ChartDataFactory()


class ModelQuery(graphene.ObjectType):
    stocks = DjangoListField(types.StockType)
    stock_by_id = graphene.Field(types.StockType, id=graphene.String())

    transactions = DjangoListField(types.TransactionType)
    transactions_filter = DjangoFilterConnectionField(types.TransactionType)
    transaction_by_id = graphene.Field(types.TransactionType, id=graphene.String())

    def resolve_stock_by_id(root, info, id):
        return Stock.objects.get(pk=id)

    def resolve_transaction_by_id(root, info, id):
        transaction = StockTransaction.objects.get(pk=id)

        if transaction.user == info.context.user:
            return transaction

        return None


class RateQuery(graphene.ObjectType):
    currency_rate = graphene.Field(
        types.CurrencyRate,
        from_currency=graphene.String(),
        to_currency=graphene.String(),
    )

    def resolve_currency_rate(root, info, from_currency, to_currency):
        rate = currency_service.get_currency_rate(from_currency, to_currency)
        return rate


class MarketQuery(graphene.ObjectType):
    stock_current_info = graphene.Field(types.StockInfoType, ticker=graphene.String())

    def resolve_stock_current_info(root, info, ticker):
        info = market_service.get_stock_info(ticker)
        return info


class ChartDataQuery(graphene.ObjectType):
    stocks_units_current_value = graphene.List(types.StockUnitsCurrentValueType)
    stock_value_history = graphene.List(
        types.StockValueHistory,
        ticker=graphene.String(),
        period=graphene.String(),
        interval=graphene.String(),
    )
    stock_transactions_value_history = graphene.Field(
        types.StockTransactionsValueHistory,
        ticker=graphene.String(),
        period=graphene.String(),
        interval=graphene.String(),
    )
    owned_stock_summary = graphene.Field(
        types.OwnedStockSummary,
        ticker=graphene.String(),
    )

    def resolve_stocks_units_current_value(root, info):
        return list(data_factory.build_stock_units_current_value(info.context.user))

    def resolve_stock_value_history(root, info, ticker, period, interval):
        return list(data_factory.build_stock_line_factory(ticker, period, interval))

    def resolve_stock_transactions_value_history(root, info, ticker, period, interval):
        history = list(data_factory.build_stock_line_factory(ticker, period, interval))
        transactions = StockTransaction.objects.filter(stock__ticker=ticker)
        currency = Stock.objects.get(ticker=ticker).currency

        return types.StockTransactionsValueHistory(history, transactions, currency)

    def resolve_owned_stock_summary(root, info, ticker):
        return data_factory.build_owned_stock_summary(info.context.user, ticker)


class Query(ModelQuery, RateQuery, MarketQuery, ChartDataQuery, graphene.ObjectType):
    pass
