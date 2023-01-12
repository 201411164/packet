import time
import threading
import subprocess
# from db import get_2_login_list, insert_emulator, update_to_available, delete_login, get_1_login_list, get_1_proxy
import subprocess
from random import random

def install_apk(apk_path, serial):
  try:
      command = "adb devices"
      process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
      devices = output.decode().split("\n")[1:-2]
      for device in devices:
        print(device)
        name = device.split("\t")[0]
        print(name)
        # if name.startswith("emulator"):
        if name == serial:
          command = f"adb -s {serial} install {apk_path}"
          process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
          output, error = process.communicate()
          print(f"Device {serial}: {output}")
  except Exception as e:
    print('설치 실패')
    print(e)



def ip_change(device):
    # control navigation bar
    print('ip 변경 시작')
    device.shell('service call statusbar 1')
    time.sleep(1.5)
    button = {"x": 34, "y": 229, "width": 126, "height": 113}
    # x, y, width, height
    # click the middle of the button
    cmdstr = 'input tap x y'
    cmdstr = cmdstr.replace('x', str(button["x"] + button["width"] / 2))
    cmdstr = cmdstr.replace('y', str(button["y"] + button["height"] / 2))
    print(cmdstr)
    device.shell(cmdstr)
    #d.click(button["x"] + button["width"] / 2, button["y"] + button["height"] / 2)
    time.sleep(3)
    device.shell(cmdstr)
    time.sleep(1)
    device.shell('service call statusbar 2')



def press_home(device):
    device.shell('input keyevent 3')
    time.sleep(3)


def launch_instagram(device):
    device.shell('am start -n com.instagram.android/com.instagram.mainactivity.MainActivity')
    time.sleep(3)


def exit_instagram(device):
    device.shell('am force-stop com.instagram.android')
    time.sleep(3)


def launch_instagram_url(device, url):
    #device.shell('am start -a android.intent.action.VIEW -d' + url)
    device.shell("am start -a android.intent.action.VIEW -d %s" % url)
    time.sleep(5)


def add_instagram_account(device, d, id, pw):
    # 로그인 정보를 받아서 인스타그램에 로그인
    # 두 가지 UI가 있어서 두 가지 경우로 나누어서 로그인

    # 만약 d(text="사용자 이름, 이메일 주소 또는 휴대폰 번호").exists() == True이면 첫번째 UI, 아니라면 두번째 UI
    if d(text="사용자 이름, 이메일 주소 또는 휴대폰 번호").exists():
        # 첫번째 UI
        # ID 입력
        d(className="android.widget.EditText", index=2).set_text(id)
        # PW 입력
        d(text="비밀번호").click()
        d.send_keys(pw, clear=True)
        time.sleep(2)
        d(text="로그인").click()
        time.sleep(5)
    else:
        if d(text="로그인").exists():
            # 두번째 UI
            # ID 입력
            d(text="로그인").click()
            time.sleep(3)
            d(resourceId="com.instagram.android:id/login_username").click()
            d.send_keys(id, clear=True)
            time.sleep(2)
            # PW 입력창 클릭
            d(resourceId="com.instagram.android:id/password_input_layout").click()
            # PW 입력
            d.send_keys(pw, clear=True)
            # 로그인 버튼 클릭
            d(resourceId="com.instagram.android:id/button_text").click()
            time.sleep(5)
        else:
            # 로그인이 되어있는 상태거나 로그인 불가
            pass



def add_instagram_account_2(device, d, id, pw):

    try:
        d(resourceId="com.instagram.android:id/profile_tab").click()
        time.sleep(1)
        d(description="옵션").click()
        time.sleep(1)
        # 설정버튼 클릭
        d.xpath('//*[@content-desc="설정"]/android.view.ViewGroup[1]').click()
        time.sleep(1)
        # 아래로 스크롤
        d.swipe(300, 500, 300, 300, 0.2)
        # d(resourceId="com.instagram.android:id/row_simple_link_textview", index=0).click()
        try:
            d(resourceId="com.instagram.android:id/row_simple_link_textview", text="계정 추가 또는 전환").click()
            time.sleep(2)
            d(resourceId="com.instagram.android:id/row_user_textview", text="계정 추가").click()
            time.sleep(2)
        except Exception as e:
            d(resourceId="com.instagram.android:id/row_simple_link_textview", text="계정 추가").click()

        # 기존 계정으로 로그인 클릭
        d(resourceId="com.instagram.android:id/bb_primary_action").click()
        time.sleep(2)
        try:
            #파란색 계정 알림 나오면 클릭
            d.xpath('//android.widget.FrameLayout[3]/android.widget.LinearLayout[1]').click()
        except:
            pass
        # 스마트락 나왔는지 체크
        time.sleep(2)
        try:
            if d(resourceId="com.google.android.gms:id/credentials_picker_title").exists():
                d(resourceId="com.google.android.gms:id/cancel").click()
                time.sleep(2)
        except:
            pass


        # 계정 변경 버튼 클릭
        d(resourceId="com.instagram.android:id/left_button").click()
        time.sleep(1)
        # ID 입력창 클릭
        d(resourceId="com.instagram.android:id/login_username").click()
        # ID 입력
        d(resourceId="com.instagram.android:id/login_username").set_text(id)
        # PW 입력창 클릭
        d(resourceId="com.instagram.android:id/password_input_layout").click()
        # PW 입력
        d.send_keys(pw, clear=True)
        # 로그인 버튼 클릭
        d(resourceId="com.instagram.android:id/button_text").click()
        time.sleep(5)

        # 만약 text="본인인지 확인해주세요" 가 나오면 뒤로가기 실행
        if d(text="본인인지 확인해주세요").exists():
            print('계정 인증 실패')
            d.press("back")
            time.sleep(1)
            # 인스타그램 종료
            exit_instagram(device)
            # DB에서 방금 로그인한 계정 삭제
            delete_login(id)
            time.sleep(3)

    except Exception as e:
        print('계정 추가 버튼 클릭 실패')
        print(e)
        return


def change_instagram_account(device, d, id):
    try:
        d(resourceId="com.instagram.android:id/profile_tab").click()
        time.sleep(1)
        d(description="옵션").click()
        time.sleep(1)
        # 설정버튼 클릭
        d.xpath('//*[@content-desc="설정"]/android.view.ViewGroup[1]').click()
        time.sleep(1)
        # 아래로 스크롤
        d.swipe(300, 500, 300, 300, 0.2)
        # d(resourceId="com.instagram.android:id/row_simple_link_textview", index=0).click()
        d(resourceId="com.instagram.android:id/row_simple_link_textview", text="계정 추가 또는 전환").click()
        # 전환할 id 버튼 클릭
        d(resourceId="com.instagram.android:id/row_user_textview", text=id).click()
        time.sleep(1)

    except Exception as e:
        print('계정 전환 실패')
        print(e)
        pass


def click_search_button(device, d, keyword, targetId):

    try:
        print('click search button 시작', keyword, targetId)
        d(resourceId="com.instagram.android:id/search_tab").click()
        time.sleep(2)
        # send keys
        d(resourceId="com.instagram.android:id/action_bar_search_hints_text_layout").click()
        d.send_keys(keyword, clear=True)
        time.sleep(3)
        if d(resourceId="com.instagram.android:id/echo_text").exists():
            d(resourceId="com.instagram.android:id/echo_text").click()

        time.sleep(4)

        # resourceId="com.instagram.android:id/image_button" 인 요소들의 description 가져오기
        imageList = []
        cnt = 0
        startRow = 1
        isFound = 0
        writerIdList = []

        while True:

            if isFound == 1:
                break

            if len(imageList) > 200 or cnt > 200:
                break
            try:
                print(cnt+1, '번째 이미지 정보')
                # imageInfo = d(resourceId='com.instagram.android:id/image_button').info
                # print(imageInfo)

                # resourceId='com.instagram.android:id/image_button' 인 요소들의 description 가져오기
                imageList = d(resourceId='com.instagram.android:id/image_button')
                print('요소 총 길이 : '+str(len(imageList)))
                for image in imageList:
                    print(image.info)
                    print(image.info['contentDescription'])
                    writerId = image.info['contentDescription'].split('님의 사진(')[0]
                    writerIdList.append(writerId)
                    if targetId in image.info['contentDescription']:
                        print('--찾았다!')
                        # contentDescription 에서 '님의 사진' 이전 부분만을 가져와 writerId에 저장
                        isFound = 1
                        d(resourceId='com.instagram.android:id/image_button', descriptionContains=targetId).click()
                        d.swipe(300, 310, 300, 320, 0.2)
                        time.sleep(10)
                        break

                d.swipe(300, 900, 300, 300, 0.2)
                d.swipe(300, 900, 300, 300, 0.2)
                d.swipe(300, 900, 300, 300, 0.2)

                print(writerIdList)

                cnt = cnt + 1

            except Exception as e:
                cnt = cnt + 1
                print('imageList error : ', e)
                print('description 가져오기 실패')

        print(imageList)

    except Exception as e:
        print(e)
    # d(resourceId="com.instagram.android:id/image_button", description="김진영님의 사진(1행, 2열)").click()
    # d(resourceId="com.instagram.android:id/action_bar_button_back").click()

    time.sleep(5)


def grant_permission(device_id):
  command = f"adb -s {device_id} shell pm grant com.kinandcarta.create.proxytoggle android.permission.WRITE_SECURE_SETTINGS"
  process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  return output, error


def set_proxy(device, d, loginList):
    press_home(device)
    d(text="Proxy Toggle").click()
    time.sleep(2)
    row = get_1_proxy(device.serial)
    ip = row[0]
    port = str(row[1])

    d.xpath(
        '//*[@resource-id="com.kinandcarta.create.proxytoggle:id/input_layout_address"]/android.widget.FrameLayout[1]').click()
    d.send_keys(ip, clear=True)
    time.sleep(1)
    d.xpath(
        '//*[@resource-id="com.kinandcarta.create.proxytoggle:id/input_layout_port"]/android.widget.FrameLayout[1]').click()
    d.send_keys(port, clear=True)
    time.sleep(1)
    d(resourceId="com.kinandcarta.create.proxytoggle:id/toggle").click()
    time.sleep(2)
    press_home(device)

    for ids in loginList:
        username = ids[0]
        print('insert_login_emulator 실행')
        print(device.serial, username, ip)
        insert_emulator(device.serial, username, ip)


def home_insta(device, d, loginList):
    print('기기 : ', device.serial + ' 에서 실행')

    press_home(device)

    # install_apk('proxy-toggle.apk', device.serial)
    #
    # result = grant_permission(device.serial)
    # print(result)
    #
    # print('proxy-toggle 실행')
    # set_proxy(device, d, loginList)
    #
    #
    # # 만약 인스타그램이 설치되어있지 않다면
    # if d(packageName="com.instagram.android").exists():
    #     print('인스타그램이 설치되어 있습니다.')
    #     time.sleep(5)
    # else: #설치되어 있지 않다면
    #     print('인스타그램이 설치되어 있지 않습니다.')
    #     try:
    #         install_apk("Instagram.apk", device.serial)
    #         time.sleep(3)
    #     except Exception as e:
    #         print(e)
    #         print('설치 실패')
    #
    #
    # # 인스타그램 실행
    # time.sleep(2)
    # print('launch instagram 실행')
    launch_instagram(device)

    # for ids in loginList:
    #    username = ids[0]
    #    password = ids[1]
    #    print('login_instagram 실행')
    #    add_instagram_account(device, d, username, password)
    #    time.sleep(5)

    # 1~5초동안 랜덤하게 대기

    time.sleep(4)

    # 일산맛집, 김진영으로 테스트 진행
    print('click search button 시작')
    targetKeyword = '일산맛집'

    targetIdList = []

    click_search_button(device, d, targetKeyword, '인스타텐')

    for ids in loginList:
        username = ids[0]
        print(ids[0]+'update_to_available 실행')
        update_to_available(username)

    print('기기 : ', device.serial + ' 에서 종료')


# def controlMultipleDevice(emulatorDeviceList, emulatorU2List):
#
#     for device, d in zip(emulatorDeviceList, emulatorU2List):
#
#         # loginList에 get_5_login_list(device.serial) 함수를 통해 가져온 로그인 정보를 저장
#         loginList = get_1_login_list(device.serial)
#         print(loginList)
#
#         time.sleep(3)
#
#         task = threading.Thread(target=home_insta, args=(device, d, loginList))
#         # Thread 실행
#         task.start()
#
#
#
#
#     # 모든 Thread가 종료되면 종료하고 True 반환
#     for task in threading.enumerate():
#         if task is threading.currentThread():
#             continue
#         task.join()
#     return True