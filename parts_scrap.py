from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
from openpyxl.workbook import Workbook
import time
import pandas as pd

import links_getter as lg
import restaurant_scrap as rs
import sql_administrator as sql


# Repeat Link Scrap


def links_getter(driver):

    driver.get("https://www.tripadvisor.com/")
    driver.implicitly_wait(5)
    driver.maximize_window()

    # Go to restaurants tab and search your city
    print()
    print("Searching the City ...")
    print()
    search_actions = ActionChains(driver)

    # Select the city to search
    search_bar = driver.find_elements_by_tag_name(
        "form")[1].find_element_by_tag_name("input")
    search_bar.send_keys("Verona, Italy")
    search_bar.send_keys(Keys.RETURN)

    time.sleep(3)

    print()
    print("Navigating to Restaurants ...")
    print()
    rest_button = driver.find_element_by_css_selector(
        "a[ data-filter-id='EATERY']")
    search_actions.move_to_element(rest_button)
    search_actions.click()
    search_actions.perform()

    time.sleep(5)

    rest_links = lg.links_getter(driver)

    return rest_links


def restaurant_scraping(rest_links):
    name = []
    trip_rat = []
    food_rat = []
    service_rat = []
    value_rat = []
    no_reviews = []
    type_food = []
    direction = []
    phone = []
    price_range = []
    website = []
    special_diets = []

    print()
    print("Scraping the Restaurants Information ...")
    print()

    rest_table = pd.DataFrame(data={"Title": ["Restaurants"]})

    with pd.ExcelWriter('New_RestaurantTest.xlsx') as writer_restaurants:  # pylint: disable=abstract-class-instantiated
        rest_table.to_excel(writer_restaurants, sheet_name="Title")

        for k, group_link in rest_links.items():
            print()
            print(f"Scraping Page {k}...")

            for link in group_link:

                try:
                    rest = rs.rest_scrap(link)

                    name.append(rest.name)
                    trip_rat.append(rest.trip_rat)
                    food_rat.append(rest.food_rat)
                    service_rat.append(rest.service_rat)
                    value_rat.append(rest.value_rat)
                    no_reviews.append(rest.no_reviews)
                    type_food.append(rest.type_food)
                    direction.append(rest.direction)
                    phone.append(rest.phone)
                    price_range.append(rest.price_range)
                    website.append(rest.website)
                    special_diets.append(rest.special_diets)

                    # Write into sqlite Database
                    sql.insert_restaurant_mysql(rest)

                    print(f"{rest.name} Done!")

                except BaseException as e:
                    print("ERROR: (main, rest_scrap)", str(e))

            print()
            print(f"Page {k} Done!")
            print()

            # Create and Save Table
            print()
            print("Creating a Table and exporting information ... ")
            print()
            rest_table = pd.DataFrame(data={"Name": name, "Trip Rating": trip_rat, "Food Rating": food_rat,
                                            "Service Rating": service_rat, "Value Rating": value_rat, "Nº Reviews": no_reviews,
                                            "Type of Food": type_food, "Direction": direction, "Phone": phone, "Website": website,
                                            "Price Range": price_range, "Special Diets": special_diets})
            # print(rest_table)
            rest_table.to_excel(writer_restaurants, sheet_name=f"Page {k}")
            name.clear()
            trip_rat.clear()
            food_rat.clear()
            service_rat.clear()
            value_rat.clear()
            no_reviews.clear()
            type_food.clear()
            direction.clear()
            phone.clear()
            price_range.clear()
            website.clear()
            special_diets.clear()

# IF SCRAP FAILS SOMEWHERE AND YOU HAVE TO RETRIEVE INFO FROM EXCEL FILES
# YOU MUST CONFIRM THAT ALL LINKS ARE SAVED INTO EXCEL FILE
# IN MY CASE I NEEDED 908 LINKS


def scrap_rest_info_from_excel_links(file):
    data = pd.ExcelFile(file)
    sheet_names = data.sheet_names

    for sheet in sheet_names[1:]:
        df = data.parse(sheet)

        # Select the range of the links
        links = df[sheet][:30]

        # IMPORTANT: REMEMBER TO SELECT IN THE RANGE BELOW THE RANGE OF THE LINKS YOU CHOOSE BEFORE
        for i in range(0, 30, 1):
            # page_name = sheet[5:]
            rest = rs.rest_scrap(links[i])
            sql.insert_restaurant_mysql(rest)


# def insert_rest_info_into_excel(i, file, page_name, rest):
#     data = pd.ExcelFile(file)

#     rest_table = pd.DataFrame(data={"Name": rest.name, "Trip Rating": rest.trip_rat, "Food Rating": rest.food_rat,
#                                     "Service Rating": rest.service_rat, "Value Rating": rest.value_rat, "Nº Reviews": rest.no_reviews,
#                                     "Type of Food": rest.type_food, "Direction": rest.direction, "Phone": rest.phone, "Website": rest.website,
#                                     "Price Range": rest.price_range, "Special Diets": rest.special_diets})

#     with pd.ExcelWriter(file) as writer_restaurants:  # pylint: disable=abstract-class-instantiated
#         rest_table.to_excel(writer_restaurants, sheet_name=page_name, startrow = i+2)

# scrap_rest_info_from_excel_links('RestLinks_BackUp.xlsx')
