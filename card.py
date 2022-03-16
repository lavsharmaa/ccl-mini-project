import serial 
import time
import psycopg2

#establish connection to MySQL. You'll have to change this for your database.
connection = psycopg2.connect(user="root",
    password="root",
    host="localhost",
    port="5432",
    database="cclproject")
cursor = connection.cursor()
#create table
user_details = """CREATE TABLE IF NOT EXISTS "users"
    (
        "username" text NOT NULL,
        "firstname" text NOT NULL,
        "lastname" text NOT NULL,
        "emailid" text NOT NULL,
        "dateofbirth" date NOT NULL,
        password text NOT NULL,
        PRIMARY KEY ("username"),
        CONSTRAINT "emailid" UNIQUE ("emailid"),
        CONSTRAINT "username" UNIQUE ("username")
    );
    """
cursor.execute(user_details)

card_details = """CREATE TABLE IF NOT EXISTS "cards"
    (
        "uid" text NOT NULL,
        "username" text NOT NULL,
        "emailid" text NOT NULL,
        amount numeric NOT NULL,
        PRIMARY KEY ("username"),
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
# cursor.execute(card_details)

transaction_details = """CREATE TABLE IF NOT EXISTS "transactions"
    (
        "uid" text NOT NULL,
        "username" text NOT NULL,
        "emailid" text NOT NULL,
        amount numeric NOT NULL,
        "createtimeStamp" date NOT NULL,
        PRIMARY KEY ("username"),
        UNIQUE ("username"),
        UNIQUE ("emailid"),
        FOREIGN KEY ("uid")
            REFERENCES "cards" ("uid") MATCH SIMPLE
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
# cursor.execute(transaction_details)
connection.commit()

device = '/dev/ttyACM0' #this will have to be changed to the serial port you are using
try:
  print("Trying...",device)
  arduino = serial.Serial(device, 9600) 
except: 
  print("Failed to connect on",device)
while True:
    time.sleep(1)
    try:
        data=arduino.readline()
        print(data)
        pieces=data.split(" ")
        try:
            cursor=dbConn.cursor()
            cursor.execute("""INSERT INTO <your table name> (ID,Member_ID,allowed_members) VALUES (NULL,%s,%s)""", (pieces[0],pieces[1]))
            dbConn.commit()
            cursor.close()
        except MySQLdb.IntegrityError:
            print("failed to insert data")
        finally:
            cursor.close()
    except:
        print("Processing")