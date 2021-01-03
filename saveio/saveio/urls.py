"""saveio URL Configuration

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
from django.contrib import admin
from django.urls import path

from graphene_django.views import GraphQLView
from savings.views import transactions_as_csv_view

from .views import PrivateGraphQLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", PrivateGraphQLView.as_view(graphiql=settings.DEBUG)),
    path("csv/", transactions_as_csv_view),
]

if settings.DEBUG:
    urlpatterns += [path("debugger/", GraphQLView.as_view(graphiql=True))]
