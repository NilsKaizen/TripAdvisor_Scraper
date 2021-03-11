import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
)

mycursor = db.cursor()

# Create a Database in MySQL
mycursor.execute("CREATE DATABASE IF NOT EXISTS scrap_rest")

db = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="database_name"
)

mycursor = db.cursor()

# Create a Table for Restaurant Information, Ratings and Aditional Information
mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
mycursor.execute("DROP TABLE IF EXISTS contact_info")
mycursor.execute("DROP TABLE IF EXISTS ratings")
mycursor.execute("DROP TABLE IF EXISTS additional_info")
mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")

mycursor.execute("""CREATE TABLE IF NOT EXISTS contact_info
                (restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                direction VARCHAR(255) DEFAULT NULL,
                phone VARCHAR(20) DEFAULT NULL,
                website VARCHAR(255) DEFAULT NULL)""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS ratings
                (restaurant_id INT NOT NULL,
                trip_rating FLOAT DEFAULT NULL,
                no_reviews INT DEFAULT NULL,
                service_rating FLOAT DEFAULT NULL,
                food_rating FLOAT DEFAULT NULL,
                value_rating FLOAT DEFAULT NULL,
                FOREIGN KEY(restaurant_id) REFERENCES contact_info(restaurant_id)) """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS additional_info
                (restaurant_id INT NOT NULL,
                type_food VARCHAR(255) DEFAULT NULL,
                special_diets VARCHAR(255) DEFAULT NULL,
                price_range VARCHAR(20) DEFAULT NULL,
                FOREIGN KEY (restaurant_id) REFERENCES contact_info(restaurant_id))""")

# mycursor.execute('USE scrap_rest')

# mycursor.execute(
#     "INSERT INTO contact_info(name, direction, phone, website) VALUES (%s, %s, %s, %s)",
#     ('name', 'direction', 'phone', 'wedsite'))

# mycursor.execute(
#     f"""INSERT INTO ratings
#             VALUES(LAST_INSERT_ID(), 5, 1000, 4, 3, 5)""")

# mycursor.execute(
#     f"""INSERT INTO additional_info
#             VALUES(LAST_INSERT_ID(), 'type_food', 'special_diets', 'range_price') """)

# db.commit()


def insert_restaurant_mysql(rest):
    try:
        mycursor.execute(
            f"INSERT INTO contact_info (name, direction, phone, website) VALUES ('{rest.name}', '{rest.direction}', '{rest.phone}', '{rest.website}')")

        mycursor.execute(
            f"""INSERT INTO ratings
                VALUES(LAST_INSERT_ID(), {rest.trip_rat}, {rest.no_reviews}, {rest.service_rat}, {rest.food_rat}, {rest.value_rat}) """)

        mycursor.execute(
            f"""INSERT INTO additional_info
                VALUES (LAST_INSERT_ID(), '{rest.type_food}', '{rest.special_diets}', '{rest.price_range}')""")

        db.commit()
    except Exception as e:
        print("ERROR: ", str(e))
