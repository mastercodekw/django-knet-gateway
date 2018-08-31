# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=250, default=None, null=True,blank=True)
    payment_id = models.CharField(max_length=250, default=None, null=True,blank=True)
    tracking_id = models.CharField(max_length=250, default=None, null=True,blank=True)
    reference = models.CharField(max_length=250, default=None, null=True,blank=True)
<<<<<<< HEAD
    total = models.FloatField(default=0.000, null=True,blank=True)
=======
    total = models.DecimalField(max_digits=10, decimal_places=3, null=True,blank=True)
>>>>>>> Fixes
    result = models.CharField(max_length=250,default=None, null=True,blank=True)
    postdate = models.DateField(default=None, null=True,blank=True)
    auth = models.CharField(max_length=250,default=None, null=True,blank=True)

    def __str__(self):
        return '<KNET R: {0} | T: {1}>'.format(self.payment_id, self.total)

