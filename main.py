from selenium import webdriver
import links_getter as lg
import restaurant_scrap as rs
import sql_administrator as sql
import data_cleaning as dc
import parts_scrap as ps

try:
    PATH = "PATH"
    driver = webdriver.Chrome(PATH)
    # Create Database
    sql.create_database_mysql()

    # Get all restaurants links from page
    rest_links = ps.links_getter(driver)

    # Restaurants Scraping

    # if this step fails due to internet connection for example go to parts_scrap/scrap_rest_info_from_excel_links
    ps.restaurant_scraping(rest_links)

    # MySQL
    sql.ponderate_ratings()
    sql.get_food_and_specials_categories()

    sql.populate_food_categories_table()
    sql.populate_special_categories_table()

except Exception as e:
    print("ERROR: (main)", str(e))
    driver.quit()
finally:
    driver.quit()

print()
print("Scraping Done!")
print()
