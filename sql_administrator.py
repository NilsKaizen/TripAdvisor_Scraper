import mysql.connector
import data_cleaning as dc

# host = "host",
# user = "username",
# password = "password",
# database = "database"

# {'host': "host",
#  'user': "username",
#  'password': "password",
#  'database': "database"}

config = {'host' : "host",
          'user' : "username",
          'password' : "password",
          'database' : "database"}

# mycursor = db.cursor()
# mycursor.close()

# Create a Database in MySQL


def create_database_mysql():
    try:
        db = mysql.connector.connect(
            host="host",
            user="username",
            password="password",
        )
        mycursor = db.cursor()

        mycursor.execute("CREATE DATABASE IF NOT EXISTS new_scrap_rest")
        mycursor.execute("USE new_scrap_rest")

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

        mycursor.close()
        db.close()
    except Exception as e:
        print("ERROR: (create_database_mysql)", str(e))


def insert_restaurant_mysql(rest):
    ''' Function to insert the data into MySQL Tables'''
    try:
        db = mysql.connector.connect(**config)
        mycursor = db.cursor()

        mycursor.execute(
            f"INSERT INTO contact_info (name, direction, phone, website) VALUES ('{rest.name}', '{rest.direction}', '{rest.phone}', '{rest.website}')")

        mycursor.execute(
            f"""INSERT INTO ratings
                VALUES(LAST_INSERT_ID(), {rest.trip_rat}, {rest.no_reviews}, {rest.service_rat}, {rest.food_rat}, {rest.value_rat}) """)

        mycursor.execute(
            f"""INSERT INTO additional_info
                VALUES (LAST_INSERT_ID(), '{rest.type_food}', '{rest.special_diets}', '{rest.price_range}')""")

        db.commit()
        mycursor.close()
        db.close()
    except Exception as e:
        print("ERROR: (insert_restaurant_mysql)", str(e))


def create_categories_tables(cat_food, cat_special):
    ''' Creates a Table with all possibilities of food and other with all possibilities of special diets '''
    try:
        db = mysql.connector.connect(**config)
        mycursor = db.cursor()

        # Create a list of strings with all categories
        cat_food_columns = [
            f"{c} ENUM('0','1') DEFAULT '0'," for c in cat_food]

        cat_special_columns = [


            f"{c} ENUM('0','1') DEFAULT '0'," for c in cat_special]

        # Create a string with the list of strings
        cat_food_columns = ' '.join(cat_food_columns)
        cat_special_columns = ' '.join(cat_special_columns)

        mycursor.execute("USE new_scrap_rest")
        mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        mycursor.execute("DROP TABLE IF EXISTS food_categories")
        mycursor.execute("DROP TABLE IF EXISTS special_categories")
        mycursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        mycursor.execute(f"""CREATE TABLE IF NOT EXISTS food_categories
                    (restaurant_id INT NOT NULL,
                    {cat_food_columns}
                    other INT NOT NULL DEFAULT '0') """)
        mycursor.execute(f"""CREATE TABLE IF NOT EXISTS special_categories
                    (restaurant_id INT NOT NULL,
                    {cat_special_columns}
                    other INT NOT NULL DEFAULT '0') """)
       
        mycursor.close()
        db.close()
    except Exception as e:
        print('ERROR (create_categories_tables): ', str(e))


def populate_food_categories_table():
    ''' Gets all types of food for each restaurant and populates food_categories table'''
    try:
        db = mysql.connector.connect(**config)
        mycursor = db.cursor()

        mycursor.execute("USE new_scrap_rest")

        mycursor.execute(
            "SELECT restaurant_id, type_food FROM additional_info")

        rest_data = mycursor.fetchall()

        for rest in rest_data:
            id = int(rest[0])
            food_list = rest[1]

            mycursor.execute(
                f"INSERT INTO food_categories (restaurant_id) VALUES ({id})")

            db.commit()

            if ',' in food_list:
                food_list = food_list.split(",")

                for cate in food_list:
                    cate = cate.strip()
                    cate = cate.lower()
                    cate = cate.replace(' ', '_')
                    cate = cate.replace('-', '_')
                    cate = cate.replace('n.a', 'n_a')

                    mycursor.execute(f"""UPDATE food_categories
                                            SET {cate} = '1' 
                                            WHERE restaurant_id={id} """)
            else:
                cate = food_list
                cate = cate.strip()
                cate = cate.lower()
                cate = cate.replace(' ', '_')
                cate = cate.replace('-', '_')
                cate = cate.replace('n.a', 'n_a')

                mycursor.execute(f"""UPDATE food_categories
                                            SET {cate} = '1' 
                                            WHERE restaurant_id={id} """)

                db.commit()
        mycursor.close()
        db.close()
    except Exception as e:
        print('ERROR: (populate_food_categories_table)', str(e))


def populate_special_categories_table():
    ''' Gets all types of special diets for each restaurant and populates special_categories table'''
    try:
        db = mysql.connector.connect(**config)
        mycursor = db.cursor()

        mycursor.execute("USE new_scrap_rest")

        mycursor.execute(
            "SELECT restaurant_id, special_diets FROM additional_info")

        rest_data = mycursor.fetchall()

        for rest in rest_data:
            id = int(rest[0])
            special_list = rest[1]

            mycursor.execute(
                f"INSERT INTO special_categories (restaurant_id) VALUES ({id})")

            db.commit()

            if ',' in special_list:
                special_list = special_list.split(",")

                for cate in special_list:
                    cate = cate.strip()
                    cate = cate.lower()
                    cate = cate.replace(' ', '_')
                    cate = cate.replace('-', '_')
                    cate = cate.replace('n.a', 'n_a')

                    mycursor.execute(f"""UPDATE special_categories
                                            SET {cate} = '1' 
                                            WHERE restaurant_id={id} """)
            else:
                cate = special_list
                cate = cate.strip()
                cate = cate.lower()
                cate = cate.replace(' ', '_')
                cate = cate.replace('-', '_')
                cate = cate.replace('n.a', 'n_a')

                mycursor.execute(f"""UPDATE special_categories
                                            SET {cate} = '1' 
                                            WHERE restaurant_id={id} """)

                db.commit()
        mycursor.close()
        db.close()
    except Exception as e:
        print('ERROR: (populate_special_categories_table)', str(e))

def ponderate_ratings():
    ''' Create a Table called ratings_ponderate to give every restaurant a status in order to it's no_ratings
    < 100 : 0
    100 <= x < 300 : 1
    300 <= x < 1000 : 2
    >= 1000: 3 '''

    try:
        db = mysql.connector.connect(**config)
        mycursor = db.cursor()

        # Create a Function that gives a ponderation based on the no_reviews
        mycursor.execute("""DROP FUNCTION IF EXISTS  ponderate_reviews;
                            CREATE FUNCTION ponderate_reviews (no_reviews INT) 
                            RETURNS INT
                            READS SQL DATA
                            DETERMINISTIC
                                BEGIN
                                DECLARE ponderation INT; 
                                    IF no_reviews < 100 THEN SET ponderation = 0;
                                    ELSEIF no_reviews BETWEEN 100 AND 300 THEN SET ponderation = 1;
                                    ELSEIF no_reviews BETWEEN 300 AND 1000 THEN SET ponderation = 2;
                                    ELSEIF no_reviews > 1000 THEN SET ponderation = 3;
                                    END IF;
                                RETURN ponderation; 
                                END 
                                 """, multi=True)
        db.commit()

        # Create Table with ponderations
        mycursor.execute("DROP TABLE IF EXISTS ratings_ponderate")
        mycursor.execute(f"""CREATE TABLE IF NOT EXISTS ratings_ponderate
                        SELECT 
                            restaurant_id,
                            no_reviews, 
                            ponderate_reviews (no_reviews) as ponderation
                        FROM ratings """)
        db.commit()

        mycursor.close()
        db.close()

    except Exception as e:
        print('ERROR: (ponderate_ratings)', str(e))


def get_food_and_specials_categories():
    ''' Gets all types of food and special diets for each restaurant and creates food_categories and special_diets tables'''
    try:
        db = mysql.connector.connect(**config)
        mycursor = db.cursor()

        mycursor.execute("USE new_scrap_rest")

        # Fetch Data from mySQL
        mycursor.execute(
            "SELECT type_food FROM additional_info")

        food_data = mycursor.fetchall()

        mycursor.execute(
            "SELECT special_diets FROM additional_info")

        special_data = mycursor.fetchall()

        # Join all data into a string
        raw_categories = ' '
        raw_special = ' '

        for row in food_data:
            raw_categories += f', {row[0]}'

        food_categories = dc.separate_types(raw_categories)
        food_categories = food_categories[1:]

        for row in special_data:
            raw_special += f', {row[0]}'

        special_categories = dc.separate_types(raw_special)
        special_categories = special_categories[1:]

        # Pass Data to create tables
        create_categories_tables(food_categories, special_categories)

        mycursor.close()
        db.close()
    except Exception as e:
        print('ERROR: (get_food_categories_table)', str(e))
