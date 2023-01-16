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
# import uiautomator2 as u2
from ppadb.client import Client as AdbClient
from requests import get
import subprocess
import multiprocessing as mp

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

def traffic_to_website(keyword, targetMid, foundCount, hitCount):
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

        time.sleep(3)
        ip_check()

        print('감지되지 않는 크롬 설정중.....잠시만 기다려주세요')
        driver = uc.Chrome(version_main=108)
        # driver의 timeout을 6초로 설정
        driver.set_page_load_timeout(10)
        # driver의 implicit wait을 10초로 설정
        driver.implicitly_wait(10)
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
                print('현재 페이지 : ', curPage, '현재 유입수 : ', foundCount , '현재 유효타수 : ', hitCount)
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
                        foundCount = foundCount + 1
                        # 90% 확률로 클릭하기
                        if random.randrange(0, 10) < 9:
                            hitCount = hitCount + 1
                            elem.click()
                            print('발견 완료 + 3~7초동안 체류하기')
                            # 새로 열린 창으로 포커스 이동
                            driver.switch_to.window(driver.window_handles[-1])
                            # 페이지 맨 아래로 천천히 스크롤
                            time.sleep(random.randrange(3, 6))
                            driver.execute_script("window.scrollBy(0, 300);")
                            time.sleep(random.randrange(1, 6))
                            driver.execute_script("window.scrollBy(0, 500);")
                            if random.randrange(0, 10) < 6:
                                time.sleep(random.randrange(2, 6))
                                driver.execute_script("window.scrollBy(0, -300);")
                                time.sleep(random.randrange(1, 6))
                                # 화면에 보이는 링크 아무거나 클릭하기
                                try:
                                    linkList = driver.find_elements(By.TAG_NAME, 'a')
                                    #linkList 중 하나를 랜덤하게 선택
                                    link = linkList[random.randrange(0, len(linkList))]
                                    if link.is_displayed():
                                        link.click()
                                        time.sleep(random.randrange(1, 5))
                                        print('총 유입건수 : ' + str(foundCount), '현재 유효타수 : ' + str(hitCount))
                                        driver.quit()
                                        return foundCount, hitCount
                                except Exception as e:
                                    print('총 유입건수 : ' + str(foundCount), '현재 유효타수 : ' + str(hitCount))
                                    driver.quit()
                                    return foundCount, hitCount
                            else:
                                print('체류 완료'+str(hitCount))
                                driver.quit()
                                print('총 유입건수 : ' + str(foundCount), '현재 유효타수 : ' + str(hitCount))
                                return foundCount, hitCount
                        else:
                            print('클릭하지 않음')
                            print('헛방 날리기')
                            # 500만큼 아래로 스크롤
                            driver.execute_script("window.scrollBy(0, 500);")
                            driver.quit()
                            isFound = True
                            print('총 유입건수 : ' + str(foundCount), '현재 유효타수 : ' + str(hitCount))
                            return foundCount, hitCount



    except Exception as e:
        print(e)
        # 만약 driver가 있다면 driver.quit 실행
        if driver:
            driver.quit()
        return foundCount, hitCount



def decimaltoAssembly(number):
    # 10진수를 assembly code 로 변환
    # 10진수를 16진수로 변환
    hexNumber = hex(number)
    print(hexNumber)

# return 60000000을 hex로 변환




if __name__ == '__main__':


    cnt = 1
    foundCount, hitCount = 0, 0
    while hitCount < 120:
        try:

            print(str(cnt)+'번째 타수 작업')
            p = mp.Process(target=traffic_to_website, args=('다다있어 청바지', '84227623335', foundCount, hitCount))
            # process의 결과로 foundCount, hitCount를 받는다.
            p.start()
            p.join()
            cnt = cnt + 1
        except Exception as e:
            print(e)
            pass

    print('총 유입건수 : ' + str(foundCount), '현재 유효타수 : ' + str(hitCount))
    print('프로그램을 종료합니다.')





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
