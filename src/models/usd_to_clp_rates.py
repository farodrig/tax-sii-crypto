from tortoise.fields import DateField, FloatField
from tortoise.models import Model


class USDToCLPRates(Model):
    date = DateField(unique=True)
    value = FloatField()
