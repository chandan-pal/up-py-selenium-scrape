# Enter the URL here
URL = 'https://www.bseindia.com/corporates/Comp_Resultsnew.aspx'

import requests
import pandas as pd
import re
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup

#headers
headers = {'Referer':'https://www.bseindia.com/corporates/Comp_Resultsnew.aspx','Accept-Encoding':'gzip, deflate, br','Accept-Language':'en-US,en;q=0.5','Accept': 'application/json, text/plain, */*','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

session = requests.Session()

#params
params={}
params.update({'ctl00$ContentPlaceHolder1$broadcastdd': '2'})
params.update({'ctl00$ContentPlaceHolder1$industrydd': 'ALL'})
params.update({'ctl00$ContentPlaceHolder1$periioddd': 'ALL'})
params.update({'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit'})

# Make a request to the base url : here also turning of SSL verification for my specific need
page = session.get(URL, headers=headers, verify=False, params=params)
print(session.cookies.get_dict())

# parse the response as html
soup = BeautifulSoup(page.content, 'html.parser')

# from response find all the td elements with class=link
instances = soup.find_all('table', id='ContentPlaceHolder1_gvData')

# print(instances)
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
            if j==5 and td.find('a') is not None:
                href = td.find('a')['href']
                params_search = re.search('javascript:__doPostBack\(\'(.*)\',\'(.*)\'\)', href)
                if params_search:
                    xbrl_params = {}
                    print(params_search.group(1))
                    xbrl_params.update({'__EVENTTARGET':params_search.group(1)})
                    xbrl_params.update({'__EVENTARGUMENT':''})
                    xbrl_params.update({'ctl00$ContentPlaceHolder1$broadcastdd': '1'})
                    xbrl_params.update({'ctl00$ContentPlaceHolder1$industrydd': 'ALL'})
                    xbrl_params.update({'ctl00$ContentPlaceHolder1$periioddd': 'ALL'})
                    xbrl_params.update({'ctl00$ContentPlaceHolder1$btnSubmit': 'Submit'})
                    xbrldata = requests.get(URL, headers=headers, verify=False, params=xbrl_params)
                    print(xbrldata.content)
                    break
                    if str(xbrldata.content).find('XBRLFILES') >= 0:
                        print('==========================')
            row_data.append(text)
        data_list.append(row_data)

df = pd.DataFrame(data_list)
df.to_csv('output.csv')
print(df)