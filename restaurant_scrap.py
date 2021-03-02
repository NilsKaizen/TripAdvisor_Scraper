from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
import links_getter as lg
import time


def rest_scrap(link):

    PATH = "C:/Program Files (x86)/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.get(link)
    time.sleep(5)

    try:
        name = driver.find_element_by_css_selector("h1._3a1XQ88S[data-test-target='top-info-header']").text
        trip_rating = driver.find_element_by_css_selector("span.r2Cf69qf").text
    except:
        name = "N.A"

    try:
        food_rat = driver.find_elements_by_css_selector("div.jT_QMHn2")[0].find_elements_by_tag_name("span")[
            2].find_element_by_tag_name("span").get_attribute("class")
        food_rat = str(food_rat)[-2:]
        food_rat = int(food_rat) / 10
    except:
        food_rat = "N.A"

    try:
        service_rat = driver.find_elements_by_css_selector("div.jT_QMHn2")[1].find_elements_by_tag_name("span")[
            2].find_element_by_tag_name("span").get_attribute("class")
        service_rat = str(service_rat)[-2:]
        service_rat = int(service_rat) / 10
    except:
        service_rat = "N.A"

    try:
        value_rat = driver.find_elements_by_css_selector("div.jT_QMHn2")[2].find_elements_by_tag_name("span")[
            2].find_element_by_tag_name("span").get_attribute("class")
        value_rat = str(value_rat)[-2:]
        value_rat = int(value_rat) / 10
    except:
        value_rat = "N.A"

    try:
        no_reviews = driver.find_element_by_css_selector("span._3Wub8auF").text
        no_reviews = no_reviews.split()[0]
    except:
        no_reviews = "N.A"

    try:
        direction = driver.find_element_by_css_selector("span._2saB_OSe").text
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
            decisor = driver.find_elements_by_css_selector("div._14zKtJkz")[i].text
            if decisor == variables[0]:
                price_range = driver.find_elements_by_css_selector("div._1XLfiSsv")[i].text
            elif decisor == variables[1]:
                type_food = driver.find_elements_by_css_selector("div._1XLfiSsv")[i].text
            elif decisor == variables[2]:
                special_diets = driver.find_elements_by_css_selector("div._1XLfiSsv")[i].text
    except:
        price_range = "N.A"
        type_food = "N.A"
        special_diets = "N.A"

    driver.quit()

    rest = Restaurant(name, trip_rating, food_rat, service_rat, value_rat,
                      no_reviews, type_food, direction, phone, website, price_range,
                      special_diets)

    # print(name, trip_rating, food_rat, service_rat, value_rat,
    #       no_reviews, type_food, direction, phone, website, price_range,
    #       special_diets)
    return rest


class Restaurant:
    """Restaurant object"""

    def __init__(self, name, trip_rating, food_rat, service_rat, value_rat,
                 no_reviews, type_food, direction, phone, website, price_range,
                 special_diets):
        self.name = name
        self.trip_rating = trip_rating
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
