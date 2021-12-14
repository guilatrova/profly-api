from django.db import models


class MonetaryField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 19
        kwargs["decimal_places"] = 10
        super().__init__(*args, **kwargs)
