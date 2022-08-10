## 코레일 로그인하기 

import warnings
warnings.filterwarnings(action='ignore')

from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from random import *

import telegram
telgm_token = '5523286949:AAH-dLh7miR9gU9aMrGUZHOOLiuRlWHm0q4'
tele_bot = telegram.Bot(token = telgm_token)

# ##코레일 ID 정보 입력
# member_num = input('코레일멤버쉽 번호 입력 : ')
# password = input('비밀 번호 입력 : ')

# ## 예매 정보 입력1
# start = input('출발지 입력 : ')
# end = input('도착지 입력 : ')
# year = input('년도 입력 (Ex.2022): ')
# month = input('월 입력 (1~12): ')
# day = input('일 입력 (1~31): ')
# hous = input('출발시간 입력 (0~23): ') #0~23 사이로 입력#
print ('여정 프리셋 입력하세요 (입력하지 않을경우 수동입력) ')
print ('[1:서울-강릉(8/6), 2:청량리-강릉(8/6), 3:강릉-서울(8/7), 4:강릉-청량리(8/7)]')
travel_preset = input('여정 프리셋 : ')

## 내 아이디로 미리 설정
## 지향이 아이디
# member_num = '1040132735'
# password = 'wlgid!9286'
# 정목 아이디
member_num = '0960000414'
password = 'dbwjdahr11!'

## 예매 정보 입력 (수동)
# start = '서울'
# end = '강릉'
# year = '2022'
# month = '8'
# day = '6'
# hours = '10'

if travel_preset == '1':
    start = '서울'
    end = '강릉'
    year = '2022'
    month = '8'
    day = '6'
    hours = '10'
elif travel_preset == '2':
    start = '청량리'
    end = '강릉'
    year = '2022'
    month = '8'
    day = '6'
    hours = '10'
elif travel_preset == '3':
    start = '강릉'
    end = '서울'
    year = '2022'
    month = '8'
    day = '7'
    hours = '15'
elif travel_preset == '4':
    start = '강릉'
    end = '청량리'
    year = '2022'
    month = '8'
    day = '7'
    hours = '15'
else :
    start = input('출발지 입력 : ')
    end = input('도착지 입력 : ')
    year = input('년도 입력 (Ex.2022): ')
    month = input('월 입력 (1~12): ')
    day = input('일 입력 (1~31): ')
    hours = input('출발시간 입력 (0~23): ') #0~23 사이로 입력#

print("출발지 : " + start)
print("도착지 : " + end)
print("일  시 : " + year +"년 " + month + "월 " + day + "일 " + hours + "시")
print("위의 정보로 예매를 시작합니다.")

## Chrome Driver 경로 지정
driverPath = r"C:/Chromedriver/chromedriver.exe" 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(driverPath, options=options) 
driver.implicitly_wait(4)
driver.get('http://www.letskorail.com/korail/com/login.do') #코레일 로그인화면 접속
time.sleep(0.5)

#코레일 멤버쉽 번호 입력
driver.find_element_by_name('txtMember').send_keys(member_num)
time.sleep(0.5)

#비밀번호 입력
driver.find_element_by_name('txtPwd').send_keys(password)

#로그인 버튼 클릭
driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div[2]/div[1]/div[1]/form[1]/fieldset/div[1]/ul/li[3]/a/img").click()
driver.implicitly_wait(3)
time.sleep(0.5)

# < pop-up창 없애기 >
time.sleep(3)
driver.window_handles    # 창 개수 확인
driver.window_handles[0] # 메인창
driver.window_handles[1] # 첫 번째 팝업 창
driver.switch_to.window(driver.window_handles[1]) # 첫 번째 팝업 창으로 제어권 옮기기
driver.close()                                    # 첫 번째 팝업 창 닫기
driver.switch_to.window(driver.window_handles[0]) # 홈 화면 으로 제어권 옮기기
time.sleep(1)

#예약 화면 이동
driver.get('http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do')
driver.implicitly_wait(3)

#예매 정보 입력
driver.find_element_by_name('txtGoStart').clear()
driver.find_element_by_name('txtGoStart').send_keys(start)
driver.find_element_by_name('txtGoEnd').clear()
driver.find_element_by_name('txtGoEnd').send_keys(end)
driver.find_element_by_name('selGoYear').send_keys(year)
driver.find_element_by_name('selGoMonth').send_keys(month)
driver.find_element_by_name('selGoDay').send_keys(day)
driver.find_element_by_name('selGoHour').send_keys(hours)

# 승차권 예매 누르기 
xpath6="/html/body/div[1]/div[3]/div/div[1]/div[2]/form/div/p/a/img"
driver.find_element_by_xpath(xpath6).click()
time.sleep(1)

# < 일반실 예매 처리 (td[6] : 일반실, td[5]:특실)>
progress = 0        ##초기 진입 : 0, 예약하기 완료시 : 1
refresh_but="/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[3]/p/a/img" ## refresh button

while progress==0:
    driver.implicitly_wait(1)
    try:
        #예약하기 or 입석+좌석 등.. 하이퍼링크가 살아있는경우
        res_but = "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[1]/td[6]/a[1]/img"
        button_type = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[1]/td[6]/a[1]/img").get_attribute('alt')
        #다를경우 하이퍼링크 포함... 그러나 하이퍼링크가 좌석선택과 예약하기이경우 a[1]로 첫번째거 선택하도록 변경해야함...
    except:
        #페이지가 늦게 뜨는 경우에 대한 Error를 대비하기위해 try문 사용.. 페이지가 늦게 뜰경우 button 좌표 지정하지 않고 새로고침하도록 처리
        try:
            res_but = "/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[1]/td[6]/img"
            button_type = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/form[1]/div/div[4]/table[1]/tbody/tr[1]/td[6]/img").get_attribute('alt')
            #매진시 하이퍼링크(a) 없이 다순 img로 표시됨
        except:
            button_type = ''
            pass

    if button_type == "예약하기":
        try:
            driver.find_element_by_xpath(res_but).click()
            driver.implicitly_wait(3)
            tele_bot.sendMessage(chat_id = '5559539231', text="KTX 예약화면을 확인하세요..!!")
            progress = 1
            print("예매를 성공했습니다.")
        except:
            pass
        break
    else:
        try:
            driver.find_element_by_xpath(refresh_but).click()
        except:
            pass
    time.sleep(uniform(1.0,2.0))
