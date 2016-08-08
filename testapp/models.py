from __future__ import unicode_literals

  # -*- coding: utf-8 -*-
from django.db import models

class Document(models.Model):
  docfile = models.FileField(upload_to='documents/%Y/%m/%d')


class StockData(models.Model):
  date = models.DateTimeField()
  open = models.DecimalField(max_digits=19, decimal_places=10)
  high = models.DecimalField(max_digits=19, decimal_places=10)
  low = models.DecimalField(max_digits=19, decimal_places=10)
  close = models.DecimalField(max_digits=19, decimal_places=10)
  volume = models.BigIntegerField()
  adj_close = models.DecimalField(max_digits=19, decimal_places=10)
  stock = models.IntegerField()