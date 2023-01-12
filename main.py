import time
import subprocess
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import instagrapi
import requests
from json.decoder import JSONDecodeError
from typing import Dict
import string
import random
from selenium.webdriver import ActionChains
import uiautomator2 as u2
from ppadb.client import Client as AdbClient
from requests import get
import subprocess

# header = Headers(
#             headers=False
#         ).generate()
#         agent = header['User-Agent']
#
#         headers = {
#             'User-Agent': f'{agent}',
#         }
from deviceControl import ip_change


def ip_check():
    try:
        ip = get("https://api.ipify.org").text
        print("현재 IP 주소 : ", ip)
        return ip
    except Exception as e:
        print("Error : ", e)
        return None


def init_device():
    subprocess.call("adb devices", shell=True)
    deviceport = 5037
    client = AdbClient(host="127.0.0.1", port=deviceport)
    devices = client.devices()
    return devices

def traffic_to_website(keyword, targetMid):
    try:
        # process = CrawlerProcess()
        # crawler = process.create_crawler(QuotesSpider)
        # process.crawl(crawler)
        # process.start()
        #
        # print('scrapy 종료')
        # driver = init_driver()
        # do_login(driver)
        # 설치한 requests를 불러옵니다
        # ip_check()
        devices = init_device()
        # realDevice는 실제 기기의 device 객체이다. 테더링을 통한 IP변경용으로 사용된다.
        realDevice = None

        # devices = init_device_remote('210.178.81.6', 5555)

        if len(devices) == 0:
            print("기기가 연결되어 있지 않습니다.")
            quit()
        # devices의 IMEI 번호 출력
        for device in devices:
            # 만약 device.serial이 emulator로 시작한다면
            if device.serial.startswith('emulator'):
                pass
            else:
                print('실제 기기입니다.')
                realDevice = device
            print(device.serial)
            print(device.get_properties())
            print('device 출력하기')

        ip_change(realDevice)
        # ip_check()

        print('감지되지 않는 크롬 설정중.....잠시만 기다려주세요')
        driver = uc.Chrome(version_main=108)
        print('크롬 실행 완료')
        driver.get('https://shopping.naver.com/home')
        # input tag이며 title attribute가 '검색어 입력'인 요소를 찾아 클릭
        driver.find_element(By.XPATH, '//input[@title="검색어 입력"]').click()
        #keyword = input('검색어를 입력하세요 : ').strip()
        #targetMid = input('Mid값을 입력하세요 : ').strip()
        # 다다있어
        # 84227623335
        # keyword 를 검색어 입력창에 입력
        driver.find_element(By.XPATH, '//input[@title="검색어 입력"]').send_keys(keyword)
        # 엔터 입력
        driver.find_element(By.XPATH, '//input[@title="검색어 입력"]').send_keys(Keys.ENTER)

        time.sleep(2)
        isFound = False
        curPage = 1

        while not isFound:
            # class='basicList_link__JLQJf' 인 요소들을 모두 찾는다.
            current_url = driver.current_url
            # https://search.shopping.naver.com/search/all?query=%EC%B2%AD%EB%B0%94%EC%A7%80&cat_id=&frm=NVSHATC
            # class='pagination_btn_page___ry_S'
            time.sleep(2)
            elemList = driver.find_elements(By.CLASS_NAME, 'basicList_link__JLQJf')
            try:
                pageElementList = driver.find_elements(By.CLASS_NAME, 'pagination_btn_page___ry_S')
                if pageElementList[0].is_displayed():
                    for page in pageElementList:
                        if str(page.text) == str(curPage + 1):
                            page.click()
                            time.sleep(3)
                else:
                    pass
            except Exception as e:
                pass

            cnt = 0
            for elem in elemList:
                cnt = cnt + 1
                print('elem의 길이 :' + str(len(elemList)))
                print('현재 elem : ' + str(cnt))
                try:
                    action = ActionChains(driver)
                    action.move_to_element(elem).perform()
                except Exception as e:
                    pass
                url = elem.get_attribute('href')
                time.sleep(random.randrange(0, 2))
                if 'Mid=' in url:
                    print(url)
                    MidValue = url.split('Mid=')[1].split('&')[0]
                    print(MidValue)
                    if MidValue == targetMid:
                        # 만약 같다면 해당 elem 클릭
                        print('발견')
                        elem.click()
                        print('현재 페이지 : ' + str(curPage))
                        isFound = True
                        print('발견 완료 + 3~7초동안 체류하기')
                        time.sleep(random.randrange(3, 7))
                        driver.quit()
                        break
    except Exception as e:
        print(e)



if __name__ == '__main__':
    cnt = 1
    while True:
        try:
            print(str(cnt)+'번쨰 타수')
            traffic_to_website('다다있어 청바지', '84227623335')
            cnt = cnt + 1
        except Exception as e:
            print(e)
            pass





def reset_password(self, username: str) -> Dict:
    """
    Reset your password
    Returns
    -------
    Dict
        Jsonified response from Instagram
    """

    response = requests.post(
        "https://www.instagram.com/accounts/account_recovery_send_ajax/",
        data={"email_or_username": username, "recaptcha_challenge_field": ""},
        headers={
            "x-requested-with": "XMLHttpRequest",
            "x-csrftoken": gen_token(),
            "Connection": "Keep-Alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
        },
        proxies=self.public.proxies,
    )
    try:
        return response.json()
    except JSONDecodeError as e:
        print(e)
        # if "/login/" in response.url:
        #     raise ClientLoginRequired(e, response=response)
        # raise ClientError(e, response=response)
