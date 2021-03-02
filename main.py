from selenium import webdriver
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

try:
    PATH = "WEB DRIVER PATH"
    driver = webdriver.Chrome(PATH)

    driver.get("https://www.tripadvisor.com/")
    driver.implicitly_wait(5)
    # driver.maximize_window()

    # Go to restaurants tab and search your city
    print()
    print("Searching the City ...")
    print()
    search_actions = ActionChains(driver)

    search_bar = driver.find_elements_by_tag_name("form")[1].find_element_by_tag_name("input")
    search_bar.send_keys("Verona, Italy")
    search_bar.send_keys(Keys.RETURN)

    time.sleep(3)

    print()
    print("Navigating to Restaurants ...")
    print()
    rest_button = driver.find_element_by_css_selector("a[ data-filter-id='EATERY']")
    search_actions.move_to_element(rest_button)
    search_actions.click()
    search_actions.perform()


    time.sleep(5)

    # Get all restaurants links from page
    rest_links = lg.links_getter(driver)

    # Restaurants Scraping
    name = []
    trip_rating = []
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

    for k, group_link in rest_links.items():
        print()
        print(f"Scraping Page {k}...")

        for link in group_link:

            rest = rs.rest_scrap(link)

            name.append(rest.name)
            trip_rating.append(rest.trip_rating)
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


            print(f"{rest.name} Done!")

        print()
        print(f"Page {k} Done!")
        print()

    # Create and Save Table
    print()
    print("Creating a Table and exporting information ... ")
    print()
    rest_table = pd.DataFrame(data={"Name" : name, "Trip Rating" : trip_rating, "Food Rating": food_rat,
                                     "Service Rating": service_rat, "Value Rating": value_rat, "Nº Reviews": no_reviews,
                                     "Type of Food": type_food, "Direction": direction, "Phone": phone, "Website": website,
                                     "Price Range": price_range, "Special Diets": special_diets})


except:
    driver.quit()
finally:
    driver.quit()

rest_table.to_excel(r'C: YOUR DESTINATION PATH \RestaurantTripAdvisor.xlsx')
print()
print("Scraping Done!")
print()

