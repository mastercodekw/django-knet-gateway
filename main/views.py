# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from e24PaymentPipe import Gateway as gw
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Urls go here.
ERROR_URL = "http://127.0.0.1:8000/error"
SUCCESS_URL = "http://127.0.0.1:8000/thank-you/"
RESPONSE_URL = "http://127.0.0.1:8000/result/"
ALIAS = "alias"

# Gateway configurations

knet = gw('resource.cgn', ALIAS)
knet.error_url = ERROR_URL
knet.response_url = RESPONSE_URL

def error_page(request,pid=None):
    pid = request.GET.get('PaymentID') or pid
    if pid:
        t = Transaction.objects.filter(payment_id=pid).first()
        if t is not None:
            return HttpResponse('Oops? there was something wrong with ur payment: %s' % t.id)
        return HttpResponse('There was an error with your request ID: %s'% pid)
    else:
        return HttpResponse('There was an error with your request')

def thankyou_page(request,pid):
    if not pid:
        return HttpResponse('There was an error with your request')
    else:
        t = Transaction.query.filter_by(payment_id=pid).first()
        if t is not None:
            return HttpResponse('Your payment was successful ID: %d' % t.id)
        return HttpResponse('There was an error with your request ID: %s'% pid)
@csrf_exempt
def result_page(request):
    pid = request.POST.get('paymentid')
    t = Transaction.objects.filter(payment_id=pid).first() or None
    if not t:
        return HttpResponse('There was an error with your request ID: %s'% pid)
    r = request.POST.get('result')
    t.result = r
    t.postdate = date(date.today().year, int(request.POST.get('postdate')[:2]), int(request.POST.get('postdate')[2:]))
    t.transaction_id = request.POST.get('tranid')
    t.tracking_id = request.POST.get('trackid')
    t.reference = request.POST.get('ref')
    t.auth = request.POST.get('auth')
    t.save()
    if r == unicode('CANCELLED') or r == unicode('NOT CAPTURED'):
        return redirect('error_page', pid=pid)
    return redirect('success_page', pid=pid)

def entry_page(request,id,total):
    t = Transaction.objects.filter(payment_id=id, result='CAPTURED').first()
    if t is not None:
        return HttpResponse('You have already paid for this order.')
    payment_id, payment_url = knet.get_payment_url().values()
    trackid = knet.trackid
    t = Transaction(tracking_id=trackid,total=total,payment_id=payment_id)
    t.save()
    return redirect(payment_url + "?PaymentID=" + payment_id)

