import mysql.connector as pymysql
from datetime import datetime

passwrd = None
db = None  
C = None

def base_check():
    check = 0
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'restaurant_management':
                cursor.execute('USE restaurant_management')
                check = 1
    if check != 1:
        create_database()

def table_check():
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'restaurant_management':
                cursor.execute('USE restaurant_management')
                cursor.execute('SHOW TABLES')
                result = cursor.fetchall()
                if len(result) <= 2:
                    create_tables()
                else:
                    print('      Booting systems...')

def create_database():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant_management")
        db.commit()
        db.close()
        print("Database 'restaurant_management' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating database: {str(e)}")

def create_tables():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd, database="restaurant_management")
        cursor = db.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tables (
                TABLE_ID INT PRIMARY KEY,
                SEATS INT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                ITEM_ID INT PRIMARY KEY,
                ITEM_NAME VARCHAR(255),
                PRICE DECIMAL(10, 2)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                ORDER_ID INT AUTO_INCREMENT PRIMARY KEY,
                TABLE_ID INT,
                ITEM_ID INT,
                QUANTITY INT,
                TOTAL_AMOUNT DECIMAL(10, 2),
                ORDER_TIME DATETIME,
                FOREIGN KEY (TABLE_ID) REFERENCES tables(TABLE_ID),
                FOREIGN KEY (ITEM_ID) REFERENCES menu_items(ITEM_ID)
            )
        """)
        
        db.commit()
        db.close()
        print("Tables 'tables', 'menu_items', and 'orders' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating tables: {str(e)}")

def add_table():
    table_id = int(input("Enter Table ID: "))
    seats = int(input("Enter Number of Seats: "))
    data = (table_id, seats)
    sql = "INSERT INTO tables (TABLE_ID, SEATS) VALUES (%s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Table added successfully...')
    except pymysql.Error as e:
        print(f"Error adding table: {str(e)}")

def view_tables():
    C.execute("SELECT * FROM tables")
    result = C.fetchall()
    for r in result:
        print(r)

def add_menu_item():
    item_id = int(input("Enter Item ID: "))
    item_name = input("Enter Item Name: ")
    price = float(input("Enter Price: "))
    data = (item_id, item_name, price)
    sql = "INSERT INTO menu_items (ITEM_ID, ITEM_NAME, PRICE) VALUES (%s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Menu item added successfully...')
    except pymysql.Error as e:
        print(f"Error adding menu item: {str(e)}")

def view_menu_items():
    C.execute("SELECT * FROM menu_items")
    result = C.fetchall()
    for r in result:
        print(r)

def record_order():
    table_id = int(input("Enter Table ID: "))
    item_id = int(input("Enter Item ID: "))
    quantity = int(input("Enter Quantity: "))
    total_amount = float(input("Enter Total Amount: "))
    order_time = datetime.now()
    data = (table_id, item_id, quantity, total_amount, order_time)
    sql = "INSERT INTO orders (TABLE_ID, ITEM_ID, QUANTITY, TOTAL_AMOUNT, ORDER_TIME) VALUES (%s, %s, %s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Order recorded successfully...')
    except pymysql.Error as e:
        print(f"Error recording order: {str(e)}")

def view_orders():
    C.execute("SELECT * FROM orders")
    result = C.fetchall()
    for r in result:
        print(r)

def main():
    global passwrd
    passwrd = input("Enter password for MySQL: ")

    base_check()
    table_check()
    
    global db, C
    db = pymysql.connect(host="localhost", user="root", password=passwrd, database="restaurant_management")
    C = db.cursor()
    
    while True:
        log = input("For LOGIN: L, Exit: X ::: ")
        if log.upper() == "L":
            while True:
                menu = input('''Add Table: AT, View Tables: VT, Add Menu Item: AMI, View Menu Items: VMI, Record Order: RO, View Orders: VO, Exit: X ::: ''')
                if menu.upper() == 'AT':
                    add_table()
                elif menu.upper() == 'VT':
                    view_tables()
                elif menu.upper() == 'AMI':
                    add_menu_item()
                elif menu.upper() == 'VMI':
                    view_menu_items()
                elif menu.upper() == 'RO':
                    record_order()
                elif menu.upper() == 'VO':
                    view_orders()
                elif menu.upper() == 'X':
                    break
                else:
                    print("Wrong Input")
                    
        elif log.upper() == "X":
            break
        else:
            print("Wrong Input")

if __name__ == "__main__":
    main()
