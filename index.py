# Enter the URL here
URL = 'https://www.bseindia.com/corporates/Comp_Resultsnew.aspx'

import requests
import pandas as pd
import re
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(URL)
main_window = driver.current_window_handle

soup = BeautifulSoup(driver.page_source, 'html.parser')

# from response find all the td elements with class=link
instances = soup.find_all('table', id='ContentPlaceHolder1_gvData')

data_list = []
for table in instances:
    trs = table.find_all('tr')
    for i in range(len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        row_data = []
        for j in range(len(tds)):
            td = tds[j]
            text = td.getText();
            if j==5:
                try:
                    href = td.find('a')['id']
                    driver.implicitly_wait(10)
                    xblri_button = driver.find_element_by_id(href)
                    xblri_button.click()
                    windows = driver.window_handles
                    if len(windows) == 2:
                        driver.switch_to.window(windows[1])
                        xblri_data = BeautifulSoup(driver.page_source, 'html.parser').find('div', id='webkit-xml-viewer-source-xml').next
                        row_data.append(xblri_data)
                        xblri_url = driver.current_url
                        text = xblri_url
                        driver.close()
                        driver.switch_to.window(main_window)
                except:
                    row_data.append('')
            row_data.append(text)
        data_list.append(row_data)

driver.switch_to.window(main_window)
driver.close()

df = pd.DataFrame(data_list)
df.to_csv('output.csv')
print(df)




