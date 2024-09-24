import requests
import json
import time
import datetime
import os

URL_AUTHENTICATION = 'http://identity.fiingroup.vn/connect/token'
URL_ROOT = 'http://df31.fiintek.com'
USERNAME = 'df.hsc@fiingroup.vn'
PASSWORD = 'z0()aloaOjed9'
TIME_DELAY_IN_SECOND = 10
LIST_URL = [
    'http://df31.fiintek.com/Company/GetCompanyCompanyGroup',
    'http://df31.fiintek.com/Company/GetIndividualPosition',
    'http://df31.fiintek.com/Company/GetIndividualShareHolder',
    'http://df31.fiintek.com/Company/GetOrganization',
    'http://df31.fiintek.com/Company/GetPerson',
    'http://df31.fiintek.com/Company/GetPersonRole',
    'http://df31.fiintek.com/CorporateAction/GetCashDividendPlan',
    'http://df31.fiintek.com/CorporateAction/GetCashDividendPayout',
    'http://df31.fiintek.com/CorporateAction/GetOwnership',
    'http://df31.fiintek.com/CorporateAction/GetStockDividendPlan',
    # 'http://df31.fiintek.com/CoveredWarrant/GetCoveredWarrant', # 500
    # 'http://df31.fiintek.com/CoveredWarrant/GetCWCompanyGroup', #500
    'http://df31.fiintek.com/Financial/GetBalanceSheet',
    'http://df31.fiintek.com/Financial/GetCashFlow',
    'http://df31.fiintek.com/Financial/GetCWProprietaryTrading',
    'http://df31.fiintek.com/Financial/GetIncomeStatement',
    'http://df31.fiintek.com/Financial/GetProprietaryTradingStock',
    'http://df31.fiintek.com/Market/GetAdjustedRatio',
    'http://df31.fiintek.com/Market/GetExchangeRate',
    # 'http://df31.fiintek.com/Market/GetCWForeignInvestor', # 500
    # 'http://df31.fiintek.com/Market/GetCwStockPrice', # 500
    'http://df31.fiintek.com/Market/GetHnxIndex',
    'http://df31.fiintek.com/Market/GetHoseForeignInvestor',
    'http://df31.fiintek.com/Market/GetHoseIndex',
    'http://df31.fiintek.com/Market/GetHoseStock',
    'http://df31.fiintek.com/Market/GetHnxForeignInvestor',
    'http://df31.fiintek.com/Market/GetHnxStock',
    'http://df31.fiintek.com/Market/GetUpcomForeignInvestor',
    'http://df31.fiintek.com/Market/GetUpcomIndex',
    'http://df31.fiintek.com/Market/GetUpcomStock',
    'http://df31.fiintek.com/Ratio/GetRatioTTM',
    'http://df31.fiintek.com/Ratio/GetRatioTTMDaily',
    'http://df31.fiintek.com/Ratio/GetReturnIndex',
    'http://df31.fiintek.com/Ratio/GetReturnStock',
]


def get_token():
    body = {
        'grant_type': 'password',
        'client_id': 'FiinTek.DataFeed.Client',
        'client_secret': 'datafeed1212',
        'scope': 'openid fiintek.datafeed',
        'username': USERNAME,
        'password': PASSWORD,
    }
    res = requests.post(URL_AUTHENTICATION, data=body)
    return json.loads(res.text)


def url_to_name(s):
    s = s.replace('http://', '')
    s = s.replace('/', '_')
    return s


def crawl(url, saved_path):
    global token
    global access_token
    global expired_token_time

    saved_folder = url_to_name(url)
    create_folder(saved_path + '/' + saved_folder)

    next_url = url + '?pageIndex=1&pageSize=100'
    while next_url is not None:
        current_time = int(time.time())
        if current_time > expired_token_time:
            token = get_token()
            access_token = token['access_token']

        res = requests.get(next_url, headers={'Authorization': f'Bearer {access_token}'})
        print(res)
        if res.status_code == 200:
            data = json.loads(res.text)
            save_data(saved_path + '/' + saved_folder + '/' + str(data['Paging']['CurrentPage']) + '.txt', res.text)
            next_url = data['Paging']['NextPageURL']
            time.sleep(TIME_DELAY_IN_SECOND)
        else:
            print(f'crawl url={next_url} fail res={res.text}')
            time.sleep(TIME_DELAY_IN_SECOND)
            break


def save_data(path, content):
    with open(path, 'w') as f:
        f.write(content)


def get_path_folder():
    now = datetime.datetime.now()
    return f"./{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}"


def create_folder(path_folder):
    if not os.path.isdir(path_folder):
        os.makedirs(path_folder)


path_folder = get_path_folder()
current = int(time.time())
create_folder(path_folder)

token = get_token()
expired_token_time = current + token['expires_in']
access_token = token['access_token']

for url in LIST_URL:
    crawl(url, path_folder)
