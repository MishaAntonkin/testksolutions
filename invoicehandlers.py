import hashlib

from flask import render_template, redirect
import requests

from configmodule import SECRET_SHOP_KEY, SHOP_ID
from logs import write_log


class InvoiceCounter:
    """Needed to assign a unique id"""
    def __init__(self):
        self.counter = 0

    def __call__(self):
        self.counter += 1
        return str(self.counter)


get_invoice_id = InvoiceCounter()


def tip(form):
    """
    get paid by tip method
    :param form:
    :return: rendered template
    """
    key_required = ['amount', 'currency', 'shop_id', 'shop_invoice_id']

    invoice_id = get_invoice_id()
    amount = '%.2f' % form.money.data
    currency = form.currencies.data
    description = form.description.data
    payload = {"description": description, "shop_invoice_id": invoice_id,
               "currency": currency, "amount": amount, "shop_id": SHOP_ID}
    sign = _get_sign(payload, key_required, SECRET_SHOP_KEY)
    payload['sign'] = sign
    write_log('success', payload)
    return render_template('invoice.html', input_fields=payload, method='post', action='https://tip.pay-trio.com/ru/')


def invoice(form, payway="payeer_eur"):
    """
    get paid by invoice method
    :param form:
    :param payway:
    :return: rendered template
    """
    key_required = ['amount', 'currency', 'payway', 'shop_id', 'shop_invoice_id']
    invoice_id = get_invoice_id()
    amount = '%.2f' % form.money.data
    currency = form.currencies.data
    description = form.description.data
    payload = {"description": description, "payway": payway, "shop_invoice_id": invoice_id,
               "currency": currency, "amount": amount, "shop_id": SHOP_ID}
    sign = _get_sign(payload, key_required, SECRET_SHOP_KEY)
    payload['sign'] = sign
    r = requests.post("https://central.pay-trio.com/invoice", json=payload)

    if r.status_code == 200:
        response_json = r.json()
    else:
        return redirect('/')

    if response_json['result'] == 'ok':
        input_fields = response_json['data']['data']
        method = response_json['data']['method']
        action = response_json['data']['source']
    else:
        msg_error = response_json['message']
        write_log('error', payload, msg_error)
        return redirect('/')
    write_log('success', payload)
    return render_template("invoice.html", method=method, input_fields=input_fields, action=action)


def _get_sign(payload, keys_required, secret):
    """form sign, from data which you want to send and secret key"""
    keys_sorted = sorted(keys_required)
    string_to_sign = ":".join([payload[k] for k in keys_sorted]) + secret
    sign = hashlib.md5(string_to_sign.encode('utf-8')).hexdigest()
    return sign
