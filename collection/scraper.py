import random
import re
import time, requests
from bs4 import BeautifulSoup
from base.config import url_config_file, ConfigHelper

agents = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]


class Scraper:
    def __init__(self, page) -> None:
        self.page = page
        url_cfg = ConfigHelper(url_config_file)
        # read config
        self.url = url_cfg.read_config('url', 'url_base') + str(self.page)
        self.headers = dict()
        self.headers['user-agent'] = random.choice(agents)
        self.headers['method'] = url_cfg.read_config('url', 'method')
        self.headers['authority'] = url_cfg.read_config('url', 'authority')
        self.headers['accept-encoding'] = url_cfg.read_config('url', 'accept-encoding')
        self.headers['accept-language'] = url_cfg.read_config('url', 'accept-language')
        self.headers['cookie'] = url_cfg.read_config('url', 'cookie')
        self.headers['referer'] = url_cfg.read_config('url', 'referer')
    def scrape_info(self):
        results = []
        trycnt = 6 # max try out
        while trycnt > 0:
            try:
                # download a website, get a Response object with a status_code property, which indicates if the pate was downloaded successfully
                time.sleep(0.1)
                response = requests.get(self.url, headers=self.headers)
                response.encoding = 'utf-8'
                html_code = response.content.decode(response.encoding)  # decoding
                soup = BeautifulSoup(html_code, 'html.parser')
                if len(list(soup.children)) >= 3:
                    body = soup.contents[3].contents[3].contents[7]
                else:
                    time.sleep(40) # avoid 403 forbiden
                    raise ConnectionResetError('No data for page: ' + str(self.page))

                for item in body.find_all('article'):
                    name = item.find('a', class_="bigger-5") # get book_name
                    address = re.search('https://.+\.com/threads/([\d]+)/profile', str(name)) # get book detail page's address
                    details = self.__retrieve_detail__(address) # scrape detailed infomation
                    data = item.find('em').get_text() # get book_data lists
                    data = re.split('/', data)
                    data.append(details.get('fav_num', '0'))
                    tags = item.find('span', class_='pull-right smaller-20') # get book_tags
                    tags = re.split('\n', tags.get_text())
                    intro = item.find_all('span', class_="smaller-5") # get book_into
                    del tags[0], tags[len(tags) - 1]
                    # turn text into integar, handle number words like '1.5k'
                    for i in range(4):
                        m = re.compile('([\d\.]+)([km]?)').match(data[i])
                        if m.group(2) == 'k':
                            data[i] = int(float(m.group(1)) * 1000)
                        elif m.group(2) == 'm':
                            data[i] = int(float(m.group(1)) * 1000000)
                        else: data[i] = int(data[i])
                    # append item tuple to result list 
                    results.append((address.group(1), name.get_text(), details.get('author', ''), intro[1].get_text(), \
                        data[0], data[1], data[2], data[3], ','.join(tags), details.get('create_time', ''), details.get('update_time', '')))
                # print('Read page ' + str(self.page) + ' successfuly, retrieved ' + str(len(results)) + ' records.')
                trycnt = 0 # Success
            except ConnectionResetError as ex:
                # print('Failed retrieving page ' + str(self.page) + ', retrying' + '.')
                trycnt -= 1 #retry
                if trycnt <= 0:
                    print('Failed retrieving page ' + str(self.page) + '.')
                    # raise(Exception('Failed retrieving page ' + str(self.page) + '.'))
                time.sleep(.5) # wait 1/2 second then retry
        return results

    def __retrieve_detail__(self, address):
        details = dict()
        trycnt = 6 # max try out
        while trycnt > 0:
            try:
                # download a website, get a Response object with a status_code property, which indicates if the pate was downloaded successfully
                time.sleep(0.1)
                response = requests.get(address.group(), headers=self.headers)
                response.encoding = 'utf-8'
                html_code = response.content.decode(response.encoding)  # decoding
                soup = BeautifulSoup(html_code, 'html.parser')
                if len(list(soup.children)) >= 3:
                    body = soup.contents[3].contents[3].contents[7].div
                else:
                    time.sleep(40) # avoid 403 forbiden
                    raise ConnectionResetError('No data for book: ' + str(address.group(1)))
                # part1 useful
                author_time = body.contents[5].contents[1]
                # part2 useful
                fav = body.contents[5].contents[3].contents[5]
                # get author name, handle anonymous case seperately
                tmp = author_time.contents[11].contents[3].contents[1].contents[3]
                if tmp.find('a'):
                    details['author'] = f'{tmp.find("a").get_text()}'  
                elif tmp.find('span', class_="majia"):
                    details['author'] = f'马甲 {tmp.find("span", class_="majia").get_text()}'
                else:
                    details['author'] = '匿名'
                # get time book created and last updated
                time_txt = author_time.find('div', class_='grayout smaller-20').get_text().strip('\n')
                m = re.compile('.*发表于(.*) ago\n.*修改于(.*) ago.*').match(time_txt) 
                if m:
                    details['create_time'] = m.group(1)
                    details['update_time'] = m.group(2)
                else:
                    m = re.compile('.*发表于(.*) ago\n.*').match(time_txt) 
                    details['create_time'] = m.group(1)
                    details['update_time'] = m.group(1)
                # get how many time books is favourited
                details['fav_num'] = fav.find_all('button')[0].find('span').get_text()
                trycnt = 0 # Success

            except ConnectionResetError as ex:
                # print('Failed retrieving book ' + str(address.group(1)) + ', retrying' + '.')
                trycnt -= 1 #retry
                if trycnt <= 0:
                    print('Failed retrieving book ' + str(address.group(1)) + '.')
                    # raise(Exception('Failed retrieving book ' + str(address.group(1)) + '.'))
                time.sleep(.5) # wait 1/2 second then retry
        return details