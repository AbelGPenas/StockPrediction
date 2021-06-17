
import requests, time, random
from bs4 import BeautifulSoup
import re
from lxml.html import fromstring
import sys

# grab a set proxies
# ----------------------------
def get_verify_proxies(url_verify:str, txt_save_path:str):
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]
    url = 'https://free-proxy-list.net/anonymous-proxy.html'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = "http://" + ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            print('Trying proxy: {}'.format(proxy))
            try:
                verify_response = requests.get(
                    url_verify,
                    proxies={'http': proxy, 'https': proxy},
                    headers={'User-Agent': random.choice(user_agent_list)}
                    , timeout=5
                )
                if verify_response.status_code == requests.codes.ok:
                    proxies.add(proxy)
                verify_response.close()
            except Exception as e:
                print(e)
                continue
            print('{} proxies have been validated'.format(len(proxies)))

    with open(txt_save_path, 'w') as f:
        for item in proxies:
            f.write("%s\n" % item)
    f.close()
    return proxies
if __name__ == '__main__':
    get_verify_proxies("https://www.marketwatch.com/markets")
