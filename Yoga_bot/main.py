from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import sys

sys.stdout = open(f"log{datetime.date.today().strftime('%Y%m%d')}.txt", 'wt')

class User:
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password


class YogaClass:
    def __init__(self, date, room, class_name, time):
        self.date = date
        self.room = room.lower().replace(' ', '_')
        self.class_name = class_name
        self.time = time

    def get_last_monday(self):
        last_monday = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        if last_monday.weekday() != 1:
            last_monday = last_monday - relativedelta(days=last_monday.weekday())
        print('Last Monday: ' + last_monday.strftime('%Y-%m-%d'))
        return last_monday.strftime('%Y-%m-%d')


def get_class_link(yoga_class, soup):
    for cell in soup.findAll('td'):
        for classes in cell.find_all('div', {'class': 'list-entry-header'}):
            if yoga_class.class_name in classes.text:
                parent_div = classes.parent
                a = parent_div.attrs.keys()
                if 'data-link' in list(parent_div.attrs.keys()):
                    if (yoga_class.time in parent_div.find('div', {'class': 'list-entry-time'}).text) & (yoga_class.date in parent_div.attrs['data-link']):
                        return parent_div.attrs['data-link']


print('Initialize driver')
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

print('Reading reservation file:')
with open('reservations.txt', 'r') as f:
    content = f.readlines()

for row in content:
    param_list = row.replace('\n', '').split(',')
    my_user = User(param_list[0], param_list[1])
    yoga_class = YogaClass(param_list[2], param_list[3], param_list[4], param_list[5])

    print('Logging')
    driver.get('https://studiojogapark.pl/strefaklienta/index.php?s=logowanie')
    driver.find_element(value='email').send_keys(my_user.user_name)
    driver.find_element(value='password').send_keys(my_user.password)
    driver.find_element(By.XPATH, '//*[@id="login_form"]/p/button').click()
    print('Finding class')
    driver.get(f'https://studiojogapark.pl/strefaklienta/index.php?s={yoga_class.room}&date={yoga_class.get_last_monday()}')

    soup = BeautifulSoup(driver.page_source, features='lxml')
    driver.get('https://studiojogapark.pl/strefaklienta/' + get_class_link(yoga_class, soup))
    radio_button = driver.find_element(By.XPATH, '//*[@id="usluga15760"]')
    driver.execute_script("arguments[0].click();", radio_button)
    driver.find_element(By.XPATH, '//*[@id="f-submit"]/button').click()

    print('Logging out')
    driver.get('https://studiojogapark.pl/strefaklienta/index.php?a=wyloguj')
