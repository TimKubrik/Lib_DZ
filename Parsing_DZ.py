from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
def write_cmc_top():
    driver = webdriver.Chrome()  # Инициализация драйвера Chrome
    driver.get('https://coinmarketcap.com/')  # Открытие страницы

    # Прокрутка и прогрузка страницы
    for i in range(15):  # Прокрутить страницу 13 раз
        driver.execute_script('window.scrollBy(0, window.innerHeight)')
        time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    list_name = soup.find_all('p', {'class': 'sc-4984dd93-0 kKpPOn'})
    list_values = soup.find_all('span', {'class': 'sc-7bc56c81-0 dCzASk'})

    data = []
    top_market_cap = 0
    for names, values in zip(list_name, list_values):
        name = names.text.strip()
        value = float(values.text.replace(',', '').replace('$', '').replace('B', '').replace('T', '').replace('M', ''))
        top_market_cap += value
        market_percentage = round(value / top_market_cap * 100, 2)
        data.append([name, value, market_percentage])

    driver.quit()  # Закрытие браузера
    return data
data = write_cmc_top()
print(data)
def write_to_csv(data):
    now = datetime.now()
    filename = f"{now.hour}.{now.minute} {now.day}.{now.month}.{now.year}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Cryptocurrency', 'Market Capitalization', '% of Top 100'])
        writer.writerows(data)

    print(f"Data saved to {filename}")

write_to_csv(data)
