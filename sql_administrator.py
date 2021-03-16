import mysql.connector

# host = "host",
# user = "username",
# password = "password",
# database = "database"

# Connect to MySQL
db = mysql.connector.connect(
    host="host",
    user="username",
    password="password",
)

mycursor = db.cursor()

# Create a Database in MySQL
mycursor.execute("CREATE DATABASE IF NOT EXISTS new_scrap_rest")

db = mysql.connector.connect(
    host="host",
    user="username",
    password="password",
    database="database"
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


def insert_restaurant_mysql(rest):
    ''' Function to insert the data into MySQL Tables'''
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
        print("ERROR: (insert_restaurant_mysql)", str(e))


def create_categories_tables(cat_food, cat_special):
    ''' Creates a Table with all possibilities of food and other with all possibilities of special diets '''
    try:
        # Create a list of strings with all categories
        cat_food_columns = [
            f"{c} ENUM('0','1') DEFAULT '0'," for c in cat_food]

        cat_special_columns = [


            f"{c} ENUM('0','1') DEFAULT '0'," for c in cat_special]

        # Create a string with the list of strings
        cat_food_columns = ' '.join(cat_food_columns)
        cat_special_columns = ' '.join(cat_special_columns)

        mycursor.execute("USE scrap_rest")

        mycursor.execute(f"""CREATE TABLE IF NOT EXISTS food_categories
                    (restaurant_id INT NOT NULL,
                    {cat_food_columns}
                    FOREIGN KEY(restaurant_id) REFERENCES contact_info(restaurant_id)) """)
        mycursor.execute(f"""CREATE TABLE IF NOT EXISTS special_categories
                    (restaurant_id INT NOT NULL,
                    {cat_special_columns}
                    FOREIGN KEY(restaurant_id) REFERENCES contact_info(restaurant_id)) """)
    except Exception as e:
        print('ERROR (create_categories_tables): ', str(e))


def populate_food_categories_table():
    ''' Gets all types of food for each restaurant and populates food_categories table'''
    try:
        mycursor.execute("USE scrap_rest")

        mycursor.execute(
            "SELECT restaurant_id, type_food FROM additional_info")

        rest_data = mycursor.fetchall()

        for rest in rest_data:
            id = int(rest[0])
            food_list = rest[1].split(',')

            mycursor.execute(
                f"INSERT INTO food_categories (restaurant_id) VALUES ({id})")

            db.commit()

            for food in food_list:
                food = food.lower()
                mycursor.execute(f"""UPDATE food_categories
                                        SET {food} = '1' 
                                        WHERE restaurant_id={id} """)

                db.commit()
    except Exception as e:
        print('ERROR: (populate_food_categories_table)', str(e))


def populate_special_categories_table():
    ''' Gets all types of food for each restaurant and populates food_categories table'''
    try:
        mycursor.execute("USE scrap_rest")

        mycursor.execute(
            "SELECT restaurant_id, special_diets FROM additional_info")

        rest_data = mycursor.fetchall()

        for rest in rest_data:
            id = int(rest[0])
            special_list = rest[1].split(',')

            mycursor.execute(
                f"INSERT INTO food_categories (restaurant_id) VALUES ({id})")

            db.commit()

            for special in special_list:
                special = special.lower()
                mycursor.execute(f"""UPDATE food_categories
                                        SET {special} = '1' 
                                        WHERE restaurant_id={id} """)

                db.commit()
    except Exception as e:
        print('ERROR: (populate_special_categories_table)', str(e))

def ponderate_ratings():
    ''' Create a Table called ratings_ponderate to give every restaurant a status in order to it's no_ratings
    < 100 : 0
    100 <= x < 300 : 1
    300 <= x < 1000 : 2
    >= 1000: 3 '''
    
    mycursor.execute("""CREATE TABLE IF NOT EXISTS ratings_ponderate
                (SELECT restaurant_id,
                IF () """)

# CHECK THIS OUT
# DELIMITER $$
# DROP FUNCTION IF EXISTS  ponderate_reviews $$
# CREATE FUNCTION ponderate_reviews(no_reviews INT) RETURNS INT
# 	BEGIN
#     DECLARE ponderation INT; 
# 		IF no_reviews < 100 THEN SET ponderation = 0;
#         ELSEIF no_reviews BETWEEN 100 AND 300 THEN SET ponderation = 1;
#         ELSEIF no_reviews BETWEEN 300 AND 1000 THEN SET ponderation = 2;
#         ELSEIF no_reviews > 1000 THEN SET ponderation = 3;
#         END IF;
# 	RETURN ponderation; 
# 	END $$
# DELIMITER ; 

# SELECT 
# 	restaurant_id,
#     no_reviews, 
#     ponderate_reviews (no_reviews) as ponderation
# FROM ratings
