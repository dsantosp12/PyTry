__author__ = 'dsantos'

from mysql.connector import Connect, errors
from datetime import datetime
from flask.ext.bcrypt import Bcrypt

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = ''
DATABASE = 'pytry'


class Database:
    """Database model."""
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

        query = ("SELECT * FROM invoices ORDER BY `id` DESC LIMIT 15".format(id))
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

        query = ("SELECT * FROM invoices WHERE `id` = {}".format(self.invoice_id))
        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return None

        response = cur.fetchall()

        conn.close()

        return response


class Admin:
    def __init__(self, name, email, user_name, password, phone, join_date, address={}):
        bcrypt = Bcrypt()
        self.name = name
        self.email = email
        self.user_name = user_name
        self.password = bcrypt.generate_password_hash(password)
        self.phone = phone
        self.address = address
        self.join_date = join_date

    def create_employee(self):
        try:
            conn = Connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        except ConnectionError as e:
            print(e)
            return False

        cur = conn.cursor()

        query = ("INSERT INTO "
                 "`administrator`(name, user_name, password, street, city, state, zipcode, phone, email, join_date)"
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
                 "".format(self.name, self.user_name, self.password, self.address['street'],
                           self.address['city'], self.address['state'], self.address['zipcode'],
                           self.phone, self.email, self.join_date))

        try:
            cur.execute(query)
        except errors.ProgrammingError as e:
            print(e)
            return False

        conn.commit()
        conn.close()

if __name__ == '__main__':
    db = Database()
    db.init()
