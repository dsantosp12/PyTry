__author__ = 'dsantos'

from mysql.connector import Connect, errors
from datetime import datetime
from flask.ext.bcrypt import Bcrypt
from flask import make_response, redirect, url_for, request, flash

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = ''
DATABASE = 'pytry'


class Database:
    """Database model with init method to set the database."""
    def __init__(self):
        pass

    @staticmethod
    def create_database():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD)
        except:
            raise ConnectionError

        cur = conn.cursor()

        query = 'CREATE DATABASE IF NOT EXISTS `pytry`'

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)

        conn.close()

    @staticmethod
    def create_business_table():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except:
            raise ConnectionError

        cur = conn.cursor()

        query = ("CREATE TABLE IF NOT EXISTS `business` (`id` INT(11) NOT NULL AUTO_INCREMENT, "
                 "`name` VARCHAR(255) NOT NULL, `street` VARCHAR(255) NOT NULL,"
                 "`city` VARCHAR(255) NOT NULL, `state` VARCHAR(255) NOT NULL,"
                 "`zipcode` VARCHAR(255) NOT NULL, `phone` VARCHAR(255) NOT NULL,"
                 "`email` VARCHAR(255) NOT NULL, `manager` VARCHAR(255) NOT NULL, PRIMARY KEY(`id`));")

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)

        conn.close()

    @staticmethod
    def create_item_table():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except:
            raise ConnectionError

        cur = conn.cursor()

        query = ("CREATE TABLE IF NOT EXISTS `items` (`id` INT(11) NOT NULL AUTO_INCREMENT, "
                 "`description` VARCHAR(255), `market_price` DECIMAL(6,2) NOT NULL, "
                 "`costumer_price` DECIMAL(6,2) NOT NULL, `distributor_price` DECIMAL(6,2) NOT NULL, "
                 "`quantity` INT(11) NOT NULL, PRIMARY KEY(`id`));")

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)

        conn.close()

    @staticmethod
    def create_costumer_table():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except:
            raise ConnectionError

        cur = conn.cursor()

        query = ("CREATE TABLE IF NOT EXISTS `costumers` (`id` INT(11) NOT NULL AUTO_INCREMENT, "
                 "`name` VARCHAR(255) NOT NULL, `street` VARCHAR(255) NOT NULL, `city` VARCHAR(255) NOT NULL,"
                 "`state` VARCHAR(255) NOT NULL, `zipcode` VARCHAR(255) NOT NULL, `phone` VARCHAR(255) NOT NULL,"
                 "`email` VARCHAR(255) NOT NULL, PRIMARY KEY(`id`));")

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)

        conn.close()

    @staticmethod
    def create_employees_table():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except:
            raise ConnectionError

        cur = conn.cursor()

        query = ("CREATE TABLE IF NOT EXISTS `employees`(`id` INT(11) NOT NULL AUTO_INCREMENT,"
                 "`name` VARCHAR(255) NOT NULL, `street` VARCHAR(255) NOT NULL, `city` VARCHAR(255) NOT NULL,"
                 "`state` VARCHAR(255) NOT NULL, `zipcode` VARCHAR(255) NOT NULL, `phone` VARCHAR(255) NOT NULL,"
                 "`email` VARCHAR(255) NOT NULL, `join_date` DATE NOT NULL, PRIMARY KEY(`id`));")

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)

        conn.close()

    @staticmethod
    def create_invoice_table():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except:
            raise ConnectionError

        cur = conn.cursor()

        query = ("CREATE TABLE IF NOT EXISTS `invoices`(`id` INT(11) NOT NULL AUTO_INCREMENT,"
                 "`invoice_id` VARCHAR(255),`costumer` VARCHAR(255) NOT NULL, `date` DATE NOT NULL,"
                 "seller VARCHAR(255) NOT NULL, `items` TEXT NOT NULL, `total` DECIMAL(6,2),"
                 "is_pending BOOLEAN NOT NULL, PRIMARY KEY(`id`));")

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)

        conn.close()

    @staticmethod
    def create_admin_table():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except:
            raise ConnectionError

        cur = conn.cursor()

        query = ("CREATE TABLE IF NOT EXISTS `administrator`(`id` INT(11) NOT NULL AUTO_INCREMENT,"
                 "`name` VARCHAR(255) NOT NULL, `user_name` VARCHAR(255) NOT NULL, `password` VARCHAR(255) NOT NULL,"
                 "`street` VARCHAR(255) NOT NULL, `city` VARCHAR(255) NOT NULL,"
                 "`state` VARCHAR(255) NOT NULL, `zipcode` VARCHAR(255) NOT NULL, `phone` VARCHAR(255) NOT NULL,"
                 "`email` VARCHAR(255) NOT NULL, `join_date` DATE NOT NULL, PRIMARY KEY(`id`));")

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)

        conn.close()

    def init(self):
        self.create_database()
        self.create_costumer_table()
        self.create_item_table()
        self.create_business_table()
        self.create_invoice_table()
        self.create_employees_table()
        self.create_admin_table()


class Business:
    """This is the business class"""
    def __init__(self, name='', phone='', manager='', email='', address={}):
        self.name = name
        self.phone = phone
        self.manager = manager
        self.email = email
        self.address = address

    def create_business(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("INSERT INTO `business`(name, street, city, state, zipcode, phone, email, manager)"
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                 "".format(self.name, self.address['street'], self.address['city'], self.address['state'],
                           self.address['zipcode'], self.phone, self.email, self.manager))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

        return True

    @staticmethod
    def erase_business(id):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("DELETE FROM business WHERE '{}' = id".format(id))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

        return True

    def business_info(self):
        full_info = ('Name: ' + self.name + ' Address: ' + self.address['street'] + ' ' + self.address['city'] + ', ' +
                     self.address['state'] + ' ' + self.address['zipcode'] + ' Phone: ' + self.phone + ' Manager: ' +
                     self.manager + ' Email: ' + self.email)
        return full_info


class Costumer:
    """This is the costumer class"""
    def __init__(self, name='', phone='', email='', address={}):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def create_costumer(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("INSERT INTO `costumers`(name, street, city, state, zipcode, phone, email)"
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                 "".format(self.name, self.address['street'], self.address['city'], self.address['state'],
                           self.address['zipcode'], self.phone, self.email))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

        return True

    @staticmethod
    def erase_costumer(id):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("DELETE FROM costumers WHERE '{}' = id".format(id))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

        return True


class Employee:
    """ This is Employee class """
    def __init__(self, name='', phone='', email='', address={}):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.join_date = datetime.now().date()

    def create_employee(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("INSERT INTO `employees`(name, street, city, state, zipcode, phone, email, join_date)"
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                 "".format(self.name, self.address['street'], self.address['city'], self.address['state'],
                           self.address['zipcode'], self.phone, self.email, self.join_date))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

    @staticmethod
    def erase_employee(id):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("DELETE FROM employees WHERE '{}' = id".format(id))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

        return True

    @staticmethod
    def get_employees():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = "SELECT * FROM employees"
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response


class Item:
    """This is the item class"""
    def __init__(self, description='', market_price=0, costumer_price=0, distributor_price=0, quantity=0):
        self.description = description
        self.market_price = market_price
        self.costumer_price = costumer_price
        self.distributor_price = distributor_price
        self.quantity = quantity

    def add_item(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("INSERT INTO `items`(description, market_price, costumer_price, distributor_price, quantity)"
                 "VALUES('{}', '{}', '{}', '{}', '{}')"
                 "".format(self.description, self.market_price, self.costumer_price, self.distributor_price,
                           self.quantity))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

        return True

    @staticmethod
    def get_items():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = "SELECT * FROM items"

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response


class Invoice:
    def __init__(self, costumer={}, date='', seller='', items='', total=0, is_pending=False, invoice_id=''):
        self.info = costumer
        self.date = date
        self.seller = seller
        self.items = items
        self.total = total
        self.pending = is_pending
        self.invoice_id = invoice_id

    def create_invoice(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("INSERT INTO `invoices`(invoice_id, costumer, date, seller, items, total, is_pending)"
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                 "".format(self.invoice_id, self.info, self.date, self.seller, self.items, self.total, self.pending))
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

        return True

    @staticmethod
    def get_price_category(id, category):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("SELECT `{}` FROM items WHERE id = '{}'".format(category, id))
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response[0][0]

    @staticmethod
    def get_item_description_by_id(id):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("SELECT `description` FROM items WHERE id = '{}'".format(id))
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response[0][0]

    @staticmethod
    def get_ten_invoices():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("SELECT * FROM invoices ORDER BY `invoice_id` DESC LIMIT 15".format(id))
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response

    def get_invoice_by_id(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("SELECT * FROM invoices WHERE `invoice_id` = {}".format(self.invoice_id))
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response

    @staticmethod
    def get_pending_invoices():
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = "SELECT * FROM invoices WHERE `is_pending` = 1"
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response

    @staticmethod
    def change_pending_status(invoce_num):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("SELECT `is_pending` FROM `invoices` "
                 "WHERE `invoice_id` = '{}'".format(invoce_num))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        is_pending = response[0][0]

        new_status = None
        if is_pending == 1:
            new_status = 0
        elif is_pending == 0:
            new_status = 1

        query = ("UPDATE `invoices` SET `is_pending` = {} "
                 "WHERE invoice_id = '{}';".format(new_status, invoce_num))
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        conn.commit()
        conn.close()

        return response


class Admin:
    def __init__(self, name='', email='', user_name='', password='', phone='', join_date='', address={}):
        self.name = name
        self.email = email
        self.user_name = user_name
        self.password = password
        self.phone = phone
        self.address = address
        self.join_date = join_date

    def create_admin(self):
        if not self.check_duplicate():
            try:
                conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
            except ConnectionError as e:
                print(e)
                return False

            cur = conn.cursor()

            bcrypt = Bcrypt()

            query = ("INSERT INTO "
                     "`administrator`(name, user_name, password, street, city, state, zipcode, phone, email, join_date)"
                     "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                     "".format(self.name, self.user_name, bcrypt.generate_password_hash(self.password),
                               self.address['street'], self.address['city'], self.address['state'],
                               self.address['zipcode'], self.phone, self.email, self.join_date))

            try:
                cur.execute(query)
            except errors.ProgrammingError as e:
                print(e)
                return False

            conn.commit()
            conn.close()

            return True
        return False

    def check_duplicate(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        # Check if username exist
        query = "SELECT * FROM `administrator` WHERE `user_name` = '{}'".format(self.user_name)

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        response = cur.fetchall()
        print(response)
        # If so, return True
        if response:
            conn.close()
            return True

        # If not, check if email exists
        query = "SELECT * FROM `administrator` WHERE `email` = '{}'".format(self.email)

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        response = cur.fetchall()
        print(response)
        if response:
            conn.close()
            return True

        conn.close()

        # If not return False
        return False

    @staticmethod
    def check_if_admin_exist():
        """This method is used to verify if at least one administrator has been setup."""
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = "SELECT * FROM `administrator`"

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.close()

        return cur.fetchall()

    def auth_admin(self):
        """Authenticate administrator trying to login."""
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = "SELECT `password` FROM `administrator` WHERE `user_name` = '{}'".format(self.user_name)

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        response = cur.fetchall()

        conn.close()

        bcrypt = Bcrypt()

        try:
            return bcrypt.check_password_hash(response[0][0], self.password)
        except IndexError:
            return False

    @staticmethod
    def create_session(name, callback, key, time):
        response = make_response(redirect(url_for(callback)))
        response.set_cookie(name, key, time)
        return response


class Security:

    @staticmethod
    def is_login(sk):
        b = Bcrypt()

        try:
            return b.check_password_hash(request.cookies['admin_session'], sk)
        except KeyError as e:
            return False

if __name__ == '__main__':
    # db = Database()
    # db.init()
    # admin = Admin()
    # admin.user_name = 'dsantos'
    # admin.password = 'Kila@toadsfla$1432'
    # print(admin.auth_admin())
    sec = Security()
    print(sec.is_login('asdfasdfasdfasd'))
