import hashlib
from collections import OrderedDict
import itertools
import json

from flask import Flask, render_template

from forms import TextForm
from configmodule import Config
from invoicehandlers import tip, invoice


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = TextForm()
    if form.validate_on_submit():
        if form.currencies.data == '840':
            return tip(form)
        else:
            return invoice(form)
        form.clearform()
    else:
        print(form.errors)
    return render_template("buypage.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
