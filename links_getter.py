from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


def links_getter(driver):
    print()
    print("Getting the Links By Page ... ")
    print()
    # Get the number of pages
    no_pages = driver.find_element_by_css_selector("div.pageNumbers")
    no_pages = [p.text for p in no_pages.find_elements_by_tag_name("a")]
    no_pages = int(no_pages[-1])

    restaurant_links = {}
    links = pd.DataFrame(data={"Title": ["Links"]})
    with pd.ExcelWriter('New_RestaurantLinks.xlsx') as writer_links:  # pylint: disable=abstract-class-instantiated
        links.to_excel(writer_links, sheet_name="Title")

        for i in range(2, no_pages + 1, 1):
            actions = ActionChains(driver)
            driver.execute_script(

                "window.scrollTo(0, document.body.scrollHeight);")

            try:
                restaurants = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "div[data-widget-type='LOCATIONS']"))
                )
                # print('Length restaurants: ', len(restaurants))
                restaurants = [r.find_element_by_tag_name("a").get_attribute("href") for r in restaurants[1:] if
                               len(r.find_elements_by_tag_name("a")) > 0]
                restaurant_links[i - 1] = restaurants

                links = pd.DataFrame(data={f"Links Page{i-1}": restaurants})
                links.to_excel(writer_links, sheet_name=f"Links Page {i-1}")
            except Exception as e:
                print("ERROR: (restaurant_links, links_getter)", e)
                print(f"Not able to get links in page {i-1}")
            finally:

                next_page = driver.find_element_by_css_selector(
                    "div.pageNumbers")
                next_page = next_page.find_element_by_css_selector(
                    f"a[data-page='{i}']")
                actions.click(next_page)
                actions.perform()
                time.sleep(5)

            print(i - 1, "Page Links Done")

    for k, v in restaurant_links.items():
        for link in v:
            if link is None:
                v.remove(link)
    # print(restaurant_links)
    print()
    print("Links Extraction Completed")
    print()
    return restaurant_links
