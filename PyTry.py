from datetime import datetime
from inspect import stack

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask.ext.bcrypt import Bcrypt
from flask.ext.mail import Mail, Message

from mysql.connector import errors

from models import Item, Costumer, Business, Invoice, Employee, Admin, Security
from tools import prepare_items

app = Flask(__name__)

b = Bcrypt()
SK = 'F*CM)@_!($":.@!#$E++)_-_;A"S;'
SK_hash = b.generate_password_hash(SK)
app.secret_key = SK
sec = Security()

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'daniel.santos@napcorps.com'
app.config["MAIL_PASSWORD"] = 'Kila@topla$1432'

mail = Mail()
mail.init_app(app)


@app.route('/')
def home():
    if Security.is_login(SK):
        return render_template('misc/home.html', title='Home')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/invoice')
def invoice():
    if Security.is_login(SK):
        return render_template('invoice/invoice.html', title='Invoice')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/invoice/create')
def create_invoice():
    if Security.is_login(SK):
        item = Item()
        employee = Employee()
        return render_template('invoice/create_invoice.html', title='Create Invoice', items=item.get_items(),
                               employees=employee.get_employees())
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/invoice/create/process', methods=('POST', 'GET'))
def create_invoice_process():

    inv = Invoice()

    try:
        inv.info = request.form['costumer']
        inv.date = datetime.strptime(request.form['date'], '%d %B, %Y')  # CONVERT STRING TO DATETIME
        category = request.form['category']
        inv.seller = request.form['seller']
        inv.invoice_id = request.form['invoice_id']
    except Exception as e:
        raise e

    try:
        inv.pending = request.form['pending']
    except Exception as e:
        inv.pending = 0

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

        # TODO: THIS IS STATIC. FIND A DYNAMIC SOLUTION CODE: 508
        if item[0][0] == '1':
            invoice.append((quantity, inv.get_item_description_by_id(1), price, subtotal))
        elif item[0][0] == '2':
            invoice.append((quantity, inv.get_item_description_by_id(2), price, subtotal))
        elif item[0][0] == '3':
            invoice.append((quantity, inv.get_item_description_by_id(3), price, subtotal))
        elif item[0][0] == '4':
            invoice.append((quantity, inv.get_item_description_by_id(3), price, subtotal))
        elif item[0][0] == '5':
            invoice.append((quantity, inv.get_item_description_by_id(3), price, subtotal))
        elif item[0][0] == '6':
            invoice.append((quantity, inv.get_item_description_by_id(3), price, subtotal))
        else:
            invoice.append((quantity, "Unidentified item. CODE: 580", price, subtotal))

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
    if Security.is_login(SK):
        return render_template('invoice/view.html', title='View Invoice')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/invoice/view/select/search/', methods=['POST', 'GET'])
def search_invoice():
    invoice_id = request.args.get('invoice_id')
    inv = Invoice()
    inv.invoice_id = invoice_id
    invoice = inv.get_invoice_by_id()

    if invoice:
        id = invoice[0][1]
        costumer = invoice[0][2]
        date = str(datetime.strftime(invoice[0][3], '%Y-%m-%d'))
        seller = invoice[0][4]
        items = invoice[0][5]
        total = invoice[0][6]
        pending = invoice[0][7]

        return redirect(url_for('print_invoice', id=id, costumer=costumer, date=date, seller=seller,
                                items=items, total=total, pending=pending))
    else:
        return redirect(url_for('select_invoice',  nfy="No found"))


@app.route('/invoice/view/select')
def select_invoice():
    if Security.is_login(SK):
        return render_template('invoice/select_invoice.html', title='Select Invoice',
                               invoices=Invoice.get_ten_invoices(), boxes_sold=Invoice.number_of_boxes_sold())
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/invoice/view/print')
def print_invoice():
    if Security.is_login(SK):
        id = request.args.get('id')
        costumer = request.args.get('costumer')
        # CONVERT STRING TO DATETIME AND DATETIME BACK TO A FORMATED STRING
        date = datetime.strftime(datetime.strptime(request.args.get('date'), '%Y-%m-%d'), '%m/%d/%Y')
        seller = request.args.get('seller')
        items = prepare_items(request.args.get('items'))
        total = request.args.get('total')
        pending = request.args.get('pending')

        return render_template('invoice/invoice_print.html', id=id, costumer=costumer, date=date,
                               seller=seller, items=items, total=total, pending=pending, title=costumer + ' - Invoice')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/invoice/delete/', methods=['POST', 'GET'])
def delete_invoice():
    invoice = request.form['invoice-1']
    vali_invoice = request.form['invoice-2']
    if invoice == '' or vali_invoice == '':
        flash("Please complete all the fields.")
        return redirect(url_for('settings'))

    if invoice == vali_invoice:
        inv = Invoice()
        inv.invoice_id = invoice

        if inv.delete_invoice():
            flash("Invoice deleted successfully.")
            return redirect(url_for('settings'))
        else:
            flash("ERROR.")
            return redirect(url_for('settings'))
    else:
        flash("Invoice number didn't match.")
        return redirect(url_for('settings'))

@app.route('/pending')
def pending():
    if Security.is_login(SK):
        return render_template('pending/pending.html', title='Pending')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/pending/view')
def view_pending():
    if Security.is_login(SK):
        return render_template('pending/select_pending.html', callback='view_pending', title='View Pending', pending=Invoice.get_pending_invoices())
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/pending/view/change', methods=['POST', 'GET'])
def change_pending_status():
    if Security.is_login(SK):
        callback = request.form['callback']
        try:
            Invoice.change_pending_status(request.form['pending_id'])
        except Exception as e:
            print(e)
            return 'Failed'
        return redirect(url_for(callback))
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/costumer')
def costumer():
    if Security.is_login(SK):
        return render_template('costumers/costumer.html', title='Costumers')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/employees')
def employees():
    if Security.is_login(SK):
        return render_template('employees/employees.html', title='Employees')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/employees/manage')
def manage_employee():
    pass


@app.route('/employees/manage/create')
def create_employee():
    if Security.is_login(SK):
        return render_template('employees/create_employee.html', title="Create Employee")
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/employees/manage/create/process', methods=['POST', 'GET'])
def create_employee_process():
    employee = Employee()

    employee.name = request.form['name']
    employee.phone = request.form['phone']
    employee.email = request.form['email']
    employee.address = {
        'street': request.form['street'],
        'city': request.form['city'],
        'state': request.form['state'],
        'zipcode': request.form['zipcode'],
    }

    if employee.create_employee():
        msg = Message()
        employee.send_email(mail, msg, app)
        return 'Success'
    else:
        raise Exception


@app.route('/employees/manage/edit')
def edit_employee():
    pass


@app.route('/employees/manage/delete')
def delete_employee():
    pass


@app.route('/settings')
def settings():
    if Security.is_login(SK):
        return render_template('settings/settings.html', title='Settings')
    return redirect(url_for('login', callback=stack()[0][3]))


@app.route('/settings/admin/create')
def create_admin():
    admin = Admin()
    if admin.check_if_admin_exist():
        if not Security.is_login(SK):
            return redirect(url_for('login', callback='create_admin'))
    return render_template('settings/create_admin.html', title="Create Administrator")


@app.route('/settings/admin/create/process', methods=['POST', 'GET'])
def create_admin_process():
    admin = Admin()
    admin.name = request.form['name']
    admin.phone = request.form['phone']
    admin.user_name = request.form['username']
    admin.password = request.form['password']
    admin.address = {
        'street': request.form['street'],
        'city': request.form['city'],
        'state': request.form['state'],
        'zipcode': request.form['zipcode'],
    }
    admin.email = request.form['email']
    admin.join_date = datetime.now()

    if admin.create_admin():
        return redirect(url_for('create_admin', flash='Administrator created successfully.'))
    else:
        raise Exception


@app.route('/login')
def login():
    if not Security.is_login(SK):
        return render_template('settings/auth_admin.html')
    return redirect(url_for('home'))


@app.route('/login/auth', methods=['POST', 'GET'])
def login_auth():
    admin = Admin()
    admin.user_name = request.form['username']
    admin.password = request.form['password']
    try:
        callback = request.form['callback']
    except Exception as e:
        print(e)
        callback = None

    if admin.auth_admin():
        if callback:
            # response = make_response(redirect(url_for('home')))
            # response.set_cookie('session', SK_hash, 500)
            return admin.create_session('admin_session', callback, SK_hash, 500)
        else:
            return redirect(url_for('home'))
    flash('Username or password incorrect.')
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found(e):
    return render_template('misc/404.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
