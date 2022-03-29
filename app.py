import serial 
import time
import psycopg2
import os, datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort, redirect, url_for, session
from flask_session import Session
import random
import math 
import os
from twilio.rest import Client

load_dotenv()
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# twilio messaging
account_sid = '<account_sid>' 
auth_token = '<auth_token>'
client = Client(account_sid, auth_token)  

device = '/dev/ttyACM0' #this will have to be changed to the serial port you are using

# azure database
# Update connection string information
host = "cclproject.postgres.database.azure.com"
dbname = "postgres"
user = "cclproject@cclproject"
password = "SmartCardSystem123"
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

@app.route('/')
def index():
    #establish connection to PostgreSQL
    # connection = psycopg2.connect(user="root",
    #     password="root",
    #     host="localhost",
    #     port="5432",
    #     database="cclproject")
    # cursor = connection.cursor()
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()
    #create table
    user_details = """CREATE TABLE IF NOT EXISTS users
        (
            "username" text NOT NULL,
            "firstname" text NOT NULL,
            "lastname" text NOT NULL,
            "emailid" text NOT NULL,
            "mobileno" text NOT NULL,
            "dateofbirth" text NOT NULL,
            "otp" text,
            password text NOT NULL,
            PRIMARY KEY ("username"),
            CONSTRAINT "emailid" UNIQUE ("emailid"),
            CONSTRAINT "username" UNIQUE ("username"),
            CONSTRAINT "mobileno" UNIQUE ("mobileno")
        );
        """
    cursor.execute(user_details)
    connection.commit()

    # sample user entry
    # sample_user = """INSERT INTO users(username, firstname, lastname, emailid,
    # mobileno, dateofbirth, password) VALUES('sample', 'Sample', 'User', 'sample@test.in',
    # '8452930878', '24-04-2001', 'sample123');"""
    # cursor.execute(sample_user)
    # connection.commit()

    card_details = """CREATE TABLE IF NOT EXISTS cards
        (
            "cardno" text NOT NULL,
            cvv numeric NOT NULL,
            "expiry" text NOT NULL,
            "username" text NOT NULL,
            "emailid" text NOT NULL,
            balance numeric NOT NULL,
            active boolean NOT NULL,
            PRIMARY KEY ("cardno"),
            UNIQUE ("username"),
            UNIQUE ("emailid"),
            FOREIGN KEY ("username")
                REFERENCES "users" ("username") MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            FOREIGN KEY ("emailid")
                REFERENCES "users" ("emailid") MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );"""
    cursor.execute(card_details)
    connection.commit()

    # card entry
    # card_entry = """INSERT INTO cards(cardno, cvv, expiry, username, emailid, balance,
    # active) VALUES('09 DF 98 B3', 123, '24/03', 'sample', 'sample@test.in', 1000, True);"""
    # cursor.execute(card_entry)
    # connection.commit()

    transaction_details = """CREATE TABLE IF NOT EXISTS transactions
        (
            "cardno" text NOT NULL,
            "username" text NOT NULL,
            "emailid" text NOT NULL,
            amount numeric NOT NULL,
            "place" text NOT NULL,
            "date" text NOT NULL,
            approved boolean NOT NULL,
            FOREIGN KEY ("cardno")
                REFERENCES "cards" ("cardno") MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            FOREIGN KEY ("username")
                REFERENCES "users" ("username") MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID,
            FOREIGN KEY ("emailid")
                REFERENCES "users" ("emailid") MATCH SIMPLE
                ON UPDATE NO ACTION
                ON DELETE NO ACTION
                NOT VALID
        );"""
    cursor.execute(transaction_details)
    connection.commit()

    # store table
    store_details = """CREATE TABLE IF NOT EXISTS stores
        (
            "susername" text NOT NULL,
            "firstname" text NOT NULL,
            "lastname" text NOT NULL,
            "semailid" text NOT NULL,
            "smobileno" text NOT NULL,
            "dateofbirth" text NOT NULL,
            password text NOT NULL,
            PRIMARY KEY ("susername"),
            CONSTRAINT "semailid" UNIQUE ("semailid"),
            CONSTRAINT "susername" UNIQUE ("susername"),
            CONSTRAINT "smobileno" UNIQUE ("smobileno")
        );
        """
    cursor.execute(store_details)
    connection.commit()

    # sample store entry
    # sample_store = """INSERT INTO stores(susername, firstname, lastname, semailid,
    # smobileno, dateofbirth, password) VALUES('store', 'Store', 'User', 'store@test.in',
    # '8452930878', '24-04-2001', 'stores123');"""
    # cursor.execute(sample_store)
    # connection.commit()

    if session.get('logged_in') == True:
        return redirect(url_for('user_dashboard'))
    else:
        return redirect(url_for('signin'))

    # sample transaction
    # sample_transaction = """INSERT INTO transactions(cardno, username, emailid,
    # amount, place, createtimeStamp) VALUES('09 DF 98 B3', 'sample', 'sample@test.in',
    # 100, 'CCD', '24-03-2022');"""
    # cursor.execute(sample_transaction)
    # connection.commit()


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        try:
            # connection = psycopg2.connect(user="root",
            #                               password="root",
            #                               host="localhost",
            #                               port="5432",
            #                               database="cclproject")
            # cursor = connection.cursor()
            connection = psycopg2.connect(conn_string)
            print("Connection established")

            cursor = connection.cursor()

            username = request.form.get("username", False)
            password_entered = request.form.get("password", False)
            record_to_search = (username,)
            sql_login_query = """SELECT users.username, users.password FROM users WHERE users.username = %s"""
            cursor.execute(sql_login_query, record_to_search)
            query = cursor.fetchone()
            username = query[0]
            password = query[1]
            print("username")
            print(username)
            print("password")
            print(password)
            connection.commit()
 
            if password_entered == password:
                session["name"] = username
                session['logged_in'] = True   
                return redirect(url_for('user_dashboard'))
            else:
                return "Some other error!s"

        except (Exception, psycopg2.Error) as error:
            print("Error in insert operation", error)

        finally:
            # closing database connection.
            if (connection):
                #cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                render_template("user/login/login.html")

    return render_template("user/login/login.html")

@app.route('/store_signin', methods=['GET', 'POST'])
def store_signin():
    if request.method == "POST":
        susername = request.form['username']
        password = request.form['password']
        print(susername, password)
        try:
            # connection = psycopg2.connect(user="root",
            #                               password="root",
            #                               host="localhost",
            #                               port="5432",
            #                               database="cclproject")
            # cursor = connection.cursor()
            connection = psycopg2.connect(conn_string)
            print("Connection established")

            cursor = connection.cursor()

            susername = request.form.get("username", False)
            password_entered = request.form.get("password", False)
            record_to_search = (susername,)
            sql_login_query = """SELECT stores.susername, stores.password FROM stores WHERE stores.susername = %s"""
            cursor.execute(sql_login_query, record_to_search)
            query = cursor.fetchone()
            susername = query[0]
            password = query[1]
            connection.commit()
 
            if password_entered == password:
                session["name"] = susername
                session['logged_in_store'] = True   
                return redirect(url_for('store_dashboard'))
            else:
                return "Some other error!s"

        except (Exception, psycopg2.Error) as error:
            print("Error in insert operation", error)

        finally:
            # closing database connection.
            if (connection):
                # cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                render_template("store/login/store_login.html")

    return render_template("store/login/store_login.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global cursor
    if request.method == "POST":
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        emailid = request.form['emailid']
        dateofbirth = request.form['dateofbirth']
        password = request.form['password']
        mobileno = request.form['mobileno']
        
        # try:
        # connection = psycopg2.connect(user="root",
        #                                   password="root",
        #                                   host="localhost",
        #                                   port="5432",
        #                                   database="cclproject")
        # cursor = connection.cursor()
        connection = psycopg2.connect(conn_string)
        print("Connection established")

        cursor = connection.cursor()

        sql_insert_query = """INSERT INTO users(
	username, firstname, lastname, emailid, mobileno, dateofbirth, password, OTP)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        record_to_insert = (username, firstname, lastname, emailid, mobileno, dateofbirth, password, 'NULL')
        print(record_to_insert)
        cursor.execute(sql_insert_query, record_to_insert)
        connection.commit()
        print("Record inserted sucessfully")
        return redirect(url_for('signin'))
    return render_template('user/register/register.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('user/forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset():
    if request.method == "POST":
        emailid = request.form['emailid']
        password = request.form['password']
        # connection = psycopg2.connect(user="root",
        #                                 password="root",
        #                                 host="localhost",
        #                                 port="5432",
        #                                 database="proctoring")
        # cursor = connection.cursor()

        connection = psycopg2.connect(conn_string)
        print("Connection established")

        cursor = connection.cursor()

        emailid = request.form.get("emailid", False)
        password = request.form.get("password", False)
        user_email = emailid 
        user_password = password
        sql = """ UPDATE users
                SET password = %s
                WHERE emailid = %s"""
        cursor.execute(sql, (user_password, user_email))
        connection.commit()
        render_template("reset_successful.html")
    return render_template("reset_successful.html")

@app.route('/user_dashboard')
def user_dashboard():
    # connection = psycopg2.connect(user="root",
    #                                       password="root",
    #                                       host="localhost",
    #                                       port="5432",
    #                                       database="cclproject")
    # cursor = connection.cursor()
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    transaction_details = """SELECT transactions.date, transactions.amount, transactions.place, transactions.approved FROM transactions where username='sample';"""
    cursor.execute(transaction_details)
    transaction_query = cursor.fetchall()
    # card details
    card_details = """SELECT cards.cardno, cards.expiry, cards.cvv, cards.balance, cards.active, cards.username FROM cards where username='sample';"""
    cursor.execute(card_details)
    card_query = cursor.fetchall()
    return render_template('user/user_dashboard.html', transaction=transaction_query, card=card_query)

@app.route('/block_card/<username>',methods = ['GET','POST'])
def block_card(username):
    # connection = psycopg2.connect(user="root",
    #                             password="root",
    #                             host="localhost",
    #                             port="5432",
    #                             database="cclproject")
    # cursor = connection.cursor()
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    username = username
    sql = """ UPDATE cards
            SET active = %s
            WHERE username = %s"""
    cursor.execute(sql, (False, username))
    connection.commit()
    return redirect(url_for('user_dashboard'))

@app.route('/unblock_card/<username>',methods = ['GET','POST'])
def unblock_card(username):
    # connection = psycopg2.connect(user="root",
    #                             password="root",
    #                             host="localhost",
    #                             port="5432",
    #                             database="cclproject")
    # cursor = connection.cursor()
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    username = username
    sql = """ UPDATE cards
            SET active = %s
            WHERE username = %s"""
    cursor.execute(sql, (True, username))
    connection.commit()
    return redirect(url_for('user_dashboard'))

@app.route('/store_dashboard')
def store_dashboard():
    # connection = psycopg2.connect(user="root",
    #                                       password="root",
    #                                       host="localhost",
    #                                       port="5432",
    #                                       database="cclproject")
    # cursor = connection.cursor()
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    transaction_details = """SELECT transactions.username, transactions.date, transactions.amount, transactions.approved FROM transactions where username='sample';"""
    cursor.execute(transaction_details)
    transaction_query = cursor.fetchall()
    return render_template('store/store_dashboard.html', transaction=transaction_query)

@app.route('/payment')
def payment():
    return render_template('payment/payment.html')

@app.route('/payment_successful')
def payment_successful():
    return render_template('payment/payment_successful.html')

@app.route('/payment_unsuccessful')
def payment_unsuccessful():
    return render_template('payment/insufficient_balance.html')

@app.route('/card_blocked')
def card_blocked():
    return render_template('payment/card_blocked.html')

@app.route('/make_payment', methods = ['GET','POST'])
def make_payment():
    # connection = psycopg2.connect(user="root",
    #                                 password="root",
    #                                 host="localhost",
    #                                 port="5432",
    #                                 database="cclproject")
    # cursor = connection.cursor()
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    if request.method == "POST":
        amount = request.form['amount']
        mobileno = request.form['mobileno']
        digits = [i for i in range(0, 10)]
        random_str = ""

        ## create a number of any length for now range = 6
        for i in range(6):
            index = math.floor(random.random() * 10)

            random_str += str(digits[index])

        ## display the otp
        print("OTP=", random_str)
        # store the OTP in the database
        sql = """ UPDATE users
            SET "otp" = %s
            WHERE mobileno = %s"""
        cursor.execute(sql, (random_str, mobileno))
        connection.commit()
        session["mobileno"] = mobileno
        session["amount"] = amount
        mobileno = "+91"+mobileno
        print("Mobile no=", mobileno)
        message = client.messages.create(  
                              messaging_service_sid='MGa9dd1f5cab1da2f0ec8b04f16446771f', 
                              body=f'Your OTP is {random_str}',      
                              to=f'{mobileno}' 
                          )
        print(message.sid)
        return render_template("payment/verify_otp.html")
    return render_template('payment/make_payment.html')

@app.route('/verify_otp', methods = ['GET','POST'])
def verify_otp():
    # connection = psycopg2.connect(user="root",
    #                                 password="root",
    #                                 host="localhost",
    #                                 port="5432",
    #                                 database="cclproject")
    # cursor = connection.cursor()
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    if request.method == "POST":
        user_otp = request.form['otp']
        mobileno = session["mobileno"]
        amount = session["amount"]
        print("mobile no=", mobileno)
        mobilenos = (mobileno,)
        select_otp = """SELECT users."otp", users.username, users.emailid FROM users where mobileno = %s;"""
        cursor.execute(select_otp, mobilenos)
        query = cursor.fetchone()
        db_otp = query[0]
        username = query[1]
        emailid = query[2]
        if user_otp == db_otp:
            print("Trying...",device)
        arduino = serial.Serial(device, 9600)
        while True:
            data=arduino.readline()
            pieces=data.splitlines()[0]
            if pieces.startswith(b"Card UID"):
                cardno= pieces.split(b":")[1]
                # converting to string
                cardnostring = str(cardno)
                # extracting card no
                exactcard = cardnostring[3:14]
                print("Exact=", exactcard)
                # check if card is active
                check_status = """SELECT cards.cardno, cards.active, cards.balance FROM cards where cardno= %s"""
                cardno = (exactcard,)
                cursor.execute(check_status, cardno)
                query = cursor.fetchone()
                status = query[1]
                balance = query[2]
                sstatus = str(status)
                ibalance = int(balance)
                print("Status=", sstatus)
                print("Int balance=", ibalance)
                if(sstatus == 'True'):
                    print("Card is active")
                    if(ibalance >= int(amount) ):
                        # deduct the amount
                        ibalance = ibalance - int(amount)
                        print("Final amount=", ibalance)
                        # update balance
                        sql = """ UPDATE cards
                                SET balance = %s
                                WHERE cardno = %s"""
                        cursor.execute(sql, (ibalance, cardno))
                        connection.commit()
                        # update transaction table
                        transaction = """INSERT INTO public.transactions(
                            cardno, username, emailid, amount, place, date, approved)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);"""
                        record_to_insert = (cardno, username, emailid, int(amount), 'CCD', '25-03-2022', True)
                        cursor.execute(transaction, record_to_insert)
                        connection.commit()
                        return render_template('payment/payment_successful.html')
                    elif (ibalance < int(amount)):
                        return render_template('payment/insufficient_balance.html')
                else:
                    return render_template('payment/card_blocked.html')
        else:
            return "Wrong OTP"
    return render_template('payment/verify_otp.html')

@app.route('/insert', methods = ['GET','POST'])
def insert_card():
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    if request.method == "POST":
        cardno = request.form['cardno']
        cvv = request.form["cvv"]
        expirydate = request.form["expirydate"]
        username = request.form["username"]
        emailid = request.form["emailid"]
        balance = request.form["balance"]
        card_entry = """INSERT INTO cards(cardno, cvv, expiry, username, emailid, balance,
        active) VALUES(%s, %s, %s, %s, %s, %s, %s);"""
        card_values = (cardno, cvv, expirydate, username, emailid, balance, True)
        cursor.execute(card_entry, card_values)
        print("Added successfully")
        connection.commit()

    return render_template('store/store_dashboard.html')

@app.route('/add_card')
def add_card():
    return render_template('store/cards/add_card.html')

@app.route('/load_balance')
def load_balance():
    return render_template('store/cards/load_balance.html')

@app.route('/balance', methods = ['GET','POST'])
def balance():
    connection = psycopg2.connect(conn_string)
    print("Connection established")

    cursor = connection.cursor()

    if request.method == "POST":
        username = request.form['username']
        amount = request.form["amount"]
        perUsername = (username,)
        # fetch the balance
        fetch = """SELECT cards.balance, cards.username FROM cards WHERE username = %s;"""
        cursor.execute(fetch, perUsername)
        query = cursor.fetchone()
        balance = query[0]
        connection.commit()
        print("Balance=", balance)
        new_balance = balance + int(amount)
        # add the balance
        add_money = """ UPDATE cards
                SET balance = %s
                WHERE username = %s"""
        cursor.execute(add_money, (new_balance, username))
        connection.commit()
        return render_template("store/store_dashboard.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')