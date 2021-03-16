from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
import links_getter as lg
import time

import sql_administrator as sql

def rest_scrap(link):

    PATH = "C:/Program Files (x86)/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.get(link)
    time.sleep(5)

    try:
        name = driver.find_element_by_css_selector(
            "h1._3a1XQ88S[data-test-target='top-info-header']").text
        name = name.replace("'", "\'")
    except:
        name = "N.A"

    try:
        trip_rat = driver.find_element_by_css_selector("span.r2Cf69qf").text
        trip_rat = float(trip_rat)
    except:
        trip_rat = None
    try:
        food_rat = driver.find_elements_by_css_selector("div.jT_QMHn2")[0].find_elements_by_tag_name("span")[
            2].find_element_by_tag_name("span").get_attribute("class")
        food_rat = str(food_rat)[-2:]
        food_rat = float(food_rat) / 10
    except:
        food_rat = None

    try:
        service_rat = driver.find_elements_by_css_selector("div.jT_QMHn2")[1].find_elements_by_tag_name("span")[
            2].find_element_by_tag_name("span").get_attribute("class")
        service_rat = str(service_rat)[-2:]
        service_rat = float(service_rat) / 10
    except:
        service_rat = None

    try:
        value_rat = driver.find_elements_by_css_selector("div.jT_QMHn2")[2].find_elements_by_tag_name("span")[
            2].find_element_by_tag_name("span").get_attribute("class")
        value_rat = str(value_rat)[-2:]
        value_rat = float(value_rat) / 10
    except:
        value_rat = None

    try:
        no_reviews = driver.find_element_by_css_selector("span._3Wub8auF").text
        no_reviews = no_reviews.split()[0]
        no_reviews = int(no_reviews.replace(",", ""))
    except:
        no_reviews = None

    try:
        direction = driver.find_element_by_css_selector("span._2saB_OSe").text
        direction = direction.replace("'", "")
    except:
        direction = "N.A"

    try:
        phone = driver.find_elements_by_css_selector("div._36TL14Jn")[-1].find_element_by_tag_name("a").get_attribute(
            "href")
        phone = str(phone).split(":")[1]
    except:
        phone = "N.A"

    try:
        website = driver.find_elements_by_css_selector("span._13OzAOXO._2VxaSjVD")[3].find_element_by_tag_name(
            "span").find_element_by_tag_name("a").get_attribute("href")
    except:
        website = "N.A"

    try:
        price_range = "N.A"
        type_food = "N.A"
        special_diets = "N.A"

        variables = ['PRICE RANGE', 'CUISINES', 'SPECIAL DIETS']
        for i in range(3):
            decisor = driver.find_elements_by_css_selector("div._14zKtJkz")[
                i].text
            if decisor == variables[0]:
                price_range = driver.find_elements_by_css_selector("div._1XLfiSsv")[
                    i].text
            elif decisor == variables[1]:
                type_food = driver.find_elements_by_css_selector("div._1XLfiSsv")[
                    i].text
            elif decisor == variables[2]:
                special_diets = driver.find_elements_by_css_selector("div._1XLfiSsv")[
                    i].text
    except Exception as e:
        print("ERROR: (rest_scrap, price_range, type_food, special_diets)", str(e))
        price_range = "N.A"
        type_food = "N.A"
        special_diets = "N.A"

    driver.quit()

    rest = Restaurant(name, trip_rat, food_rat, service_rat, value_rat,
                      no_reviews, type_food, direction, phone, website, price_range,
                      special_diets)

    # print()
    # print(rest.name, type(rest.name))
    # print(rest.trip_rat, type(rest.trip_rat))
    # print(rest.food_rat, type(rest.food_rat))
    # print(rest.service_rat, type(rest.service_rat))
    # print(rest.value_rat, type(rest.value_rat))
    # print(rest.no_reviews, type(rest.no_reviews))
    # print(rest.type_food, type(rest.type_food))
    # print(rest.direction, type(rest.direction))
    # print(rest.phone, type(rest.phone))
    # print(rest.price_range, type(rest.price_range))
    # print(rest.website, type(rest.website))
    # print(rest.special_diets, type(rest.special_diets))
    # print()

    return rest


class Restaurant:
    """Restaurant object"""

    def __init__(self, name, trip_rat, food_rat, service_rat, value_rat,
                 no_reviews, type_food, direction, phone, website, price_range,
                 special_diets):
        self.name = name
        self.trip_rat = trip_rat
        self.food_rat = food_rat
        self.service_rat = service_rat
        self.value_rat = value_rat
        self.no_reviews = no_reviews
        self.type_food = type_food
        self.direction = direction
        self.phone = phone
        self.price_range = price_range
        self.website = website
        self.special_diets = special_diets


# rest = rest_scrap(
#     "https://www.tripadvisor.com/Restaurant_Review-g187871-d2272025-Reviews-Ristorante_Pizzeria_Nastro_Azzurro-Verona_Province_of_Verona_Veneto.html#REVIEWS")

# sql.insert_restaurant_mysql(rest)
