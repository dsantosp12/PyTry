from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from models import Item, Costumer, Business, Invoice, Employee
from tools import prepare_items

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('misc/home.html', title='Home')


@app.route('/invoice')
def invoice():
    return render_template('invoice/invoice.html', title='Invoice')


@app.route('/invoice/create')
def create_invoice():
    item = Item()
    employee = Employee()
    return render_template('invoice/create_invoice.html', title='Create Invoice', items=item.get_items(),
                           employees=employee.get_employees())


@app.route('/invoice/create/process', methods=('POST', 'GET'))
def create_invoice_process():

    inv = Invoice()

    try:
        inv.info = request.form['business_name']
        inv.date = datetime.strptime(request.form['date'], '%d %B, %Y')  # CONVERT STRING TO DATETIME
        category = request.form['category']
        inv.pending = request.form['pending']
        inv.seller = request.form['seller']
    except Exception as e:
        raise e

    items_list_id_quantity = []
    for x in range(1, 6):
        try:
            items_list_id_quantity.append((request.form['id'+str(x)], request.form['quantity'+str(x)]))
        except Exception as e:
            print(e)

    items_full = []
    for item in items_list_id_quantity:

        if item[0]:
            # LIST OF TUPLES WITH (ID, PRICE, QUANTITY )
            items_full.append((item[0], inv.get_price_category(item[0], category), item[1]))

    total = 0
    invoice = []
    for item in items_full:
        subtotal = 0
        quantity = int(item[2])
        price = int(item[1])
        subtotal = quantity * price
        total += subtotal

        if item[0][0] == '1':
            invoice.append((quantity, inv.get_item_description_by_id(1), price, subtotal))
        elif item[0][0] == '2':
            invoice.append((quantity, inv.get_item_description_by_id(2), price, subtotal))
        elif item[0][0] == '3':
            invoice.append((quantity, inv.get_item_description_by_id(3), price, subtotal))

    invoice_list = ""
    for k in invoice:
        invoice_list += str(k)
    inv.items = invoice_list.replace("'", "")
    inv.total = total

    try:
        inv.create_invoice()
    except Exception as e:
        print(e)
        return redirect(url_for('create_invoice', flash="Invoice couldn't been created."))

    return redirect(url_for('create_invoice', flash='Invoice created successfully.'))


@app.route('/invoice/view')
def view_invoices():
    return render_template('invoice/view.html', title='View Invoice')


@app.route('/invoice/view/select')
def select_invoice():
    inv = Invoice()
    return render_template('invoice/select_invoice.html', invoices=inv.get_all_invoices())


@app.route('/invoice/view/print')
def print_invoice():

    id = request.args.get('id')
    costumer = request.args.get('costumer')
    # CONVERT STRING TO DATETIME AND DATETIME BACK TO A FORMATED STRING
    date = datetime.strftime(datetime.strptime(request.args.get('date'), '%Y-%m-%d'), '%m/%d/%Y')
    seller = request.args.get('seller')
    items = prepare_items(request.args.get('items'))
    total = request.args.get('total')
    pending = request.args.get('pending')

    return render_template('invoice/invoice_print.html', id=id, costumer=costumer, date=date,
                           seller=seller, items=items, total=total, pending=pending, title=costumer + ' Invoice')


@app.route('/pending')
def pending():
    return render_template('pending/pending.html', title='Pending')


@app.route('/costumer')
def costumer():
    return render_template('costumers/costumer.html', title='Costumers')


@app.route('/employees')
def employees():
    return render_template('employees/employees.html', title='Employees')


@app.route('/settings')
def settings():
    return render_template('settings/settings.html', title='Settings')


if __name__ == '__main__':
    app.run(debug=True)
