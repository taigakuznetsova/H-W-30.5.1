import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password
chromedriver_autoinstaller.install()
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    driver.get('https://petfriends.skillfactory.ru/login')

    driver.maximize_window()
    yield driver

    driver.quit()


def test_show_all_pets(driver):
   driver.find_element(By.ID, 'email').send_keys(valid_email)

   driver.find_element(By.ID, 'pass').send_keys(valid_password)

   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a[1]').click()


   images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0

      driver.quit()


def test_all_my_pets(driver):
    driver.find_element(By.ID, 'email').send_keys(valid_email)

    driver.find_element(By.ID, 'pass').send_keys(valid_password)

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    wait = WDW(driver, 10)

    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a[1]').click()

    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h2'), "All"))

    css_locator = 'tbody>tr'
    data_my_pets = driver.find_elements(By.CSS_SELECTOR, css_locator)

    for i in range(len(data_my_pets)):
        assert wait.until(EC.visibility_of(data_my_pets[i]))

        image_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[1]')
        for i in range(len(image_my_pets)):
            if image_my_pets[i].get_attribute('src') != '':
                assert wait.until(EC.visibility_of(image_my_pets[i]))

        name_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[2]')
        for i in range(len(name_my_pets)):
            assert wait.until(EC.visibility_of(name_my_pets[i]))

        type_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[3]')
        for i in range(len(type_my_pets)):
            assert wait.until(EC.visibility_of(type_my_pets[i]))

        age_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/thead[1]/tr[1]/th[4]')
        for i in range(len(age_my_pets)):
            assert wait.until(EC.visibility_of(age_my_pets[i]))

        all_statistics = driver.find_element(By.XPATH, 'body/div[1]/div[1]/div[1]').text.split("\n")
        statistics_pets = all_statistics[1].split(" ")
        all_my_pets = int(statistics_pets[-1])
        assert len(data_my_pets) == all_my_pets


        m = 0
        for i in range(len(image_my_pets)):
            if image_my_pets[i].get_attribute('src') != '':
                m += 1
        assert m >= all_my_pets / 2

        for i in range(len(name_my_pets)):
            assert name_my_pets[i].text != ''

        for i in range(len(type_my_pets)):
            assert type_my_pets[i].text != ''

        for i in range(len(age_my_pets)):
            assert age_my_pets[i].text != ''

        list_name_my_pets = []
        for i in range(len(name_my_pets)):
            list_name_my_pets.append(name_my_pets[i].text)
        set_name_my_pets = set(list_name_my_pets)
        assert len(list_name_my_pets) == len(set_name_my_pets)

        list_data_my_pets = []
        for i in range(len(data_my_pets)):
            list_data = data_my_pets[i].text.split("\n")
            list_data_my_pets.append(list_data[0])
        set_data_my_pets = set(list_data_my_pets)
        assert len(list_data_my_pets) == len(set_data_my_pets)


