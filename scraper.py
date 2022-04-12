from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from mongo_db import collection

uybor_url = [
    'https://uybor.uz/ru/prodazha-kvartir/nedvizhimost-v-tashkente/novostroyki-v-tashkente',
]

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    

def get_contact():
    try:
        driver.find_element_by_css_selector("button.btn.btn-primary.--icon-left").click()
        phone = driver.find_element_by_tag_name("a").text
        driver.find_element_by_css_selector("button.btn.btn-secondary").click()
        return phone
    except:
        sleep(5)
        return get_contact()
       

def Convert(lst):
    res_dct = {lst[i].text: lst[i + 1].text for i in range(0, len(lst), 2)}
    del res_dct['Print']
    del res_dct['Complain']
    return res_dct


def get_data():
    
    url = f"https://uybor.uz/en/prodazha-kvartir/nedvizhimost-v-tashkente/novostroyki-v-tashkente"
    driver.get(url)
    items = driver.find_elements_by_css_selector("a.listing__link")
    imgs = []
    for item in items:
        item.click()
        driver.switch_to.window(driver.window_handles[-1])
        title = driver.find_elements_by_css_selector("h1.listing__title")[0].text
        price = driver.find_elements_by_css_selector("div.listing__price")[1].text
        elems = driver.find_elements_by_class_name("listing__img")
        for img in elems:
            if img.tag_name == "img":
                src = img.get_attribute("src")
                imgs.append(src)
        discription = driver.find_elements_by_tag_name('p')[6].text
        location = driver.find_element_by_css_selector("div.col.align-self-center").text
        # contact = get_contact()
        features = driver.find_elements_by_tag_name('td')
        features = Convert(features)        

        uybor_data = {
            'title': title,
            'price':price,
            'imgs': imgs,
            # 'contacts': contact,
            'discription': discription,
            'location': location,
            'overview': features,
        }

        collection.insert_one(uybor_data)
        sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    driver.quit()

get_data()