"""profly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import include, path

from graphene_django.views import GraphQLView

from stocks.views import transactions_as_csv_view

from . import views as core_views

urlpatterns = [
    path("", core_views.index),
    path("health/", include("health_check.urls")),
    path("graphql/", core_views.PrivateGraphQLView.as_view(graphiql=False)),
    path("csv/", transactions_as_csv_view),
]

if settings.DEBUG:
    urlpatterns += [path("debugger/", GraphQLView.as_view(graphiql=True))]
