import warnings
warnings.filterwarnings(action='ignore')
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import urllib.request
month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

## 로그인 ID/PW 기록 (혜원 아이디)
# login_id = 'neck975'
# login_pw = 'wjdahr11'
login_id = 'hyewon00315'
login_pw = 'zhel1015!'


## Chrome Driver 경로 지정
driverPath = r"chromedriver.exe" 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(driverPath, options=options) 
driver.implicitly_wait(4)

##yes24티켓 접속
driver.get('http://ticket.yes24.com/') 
time.sleep(1)

##콘서트 버튼 클릭
driver.find_element("xpath","/html/body/form/div[6]/header/div[3]/h2[1]/a").click()
time.sleep(1)
##로그인 버튼 클릭
driver.find_element("xpath","/html/body/div[4]/div/div[2]/a[1]").click()
time.sleep(1)
#ID/PW 입력 및 로그인
driver.find_element("name",'SMemberID').send_keys(login_id)
time.sleep(1)
driver.find_element("name",'SMemberPassword').send_keys(login_pw)
time.sleep(1)
driver.find_element("xpath","/html/body/div[1]/div[2]/div/div[1]/div[2]/form/fieldset/button/span/em").click()
time.sleep(1)

##페이지 이동(NCT 공연 url로 수정 필요)
driver.get('http://ticket.yes24.com/Special/43155')
time.sleep(1)

target_mon = 8
target_day = 17
target_hour = 19
target_min = 59
target_sec = 59

progress = 0

print(f'{target_mon}월 {target_day}일 {target_hour}시 {target_min}분 {target_sec}초에 예약을 시도합니다.')

url = 'http://ticket.yes24.com'
date = urllib.request.urlopen(url).headers['Date'][5:-4]
day, mon, hour, min, sec = int(date[:2]), int(month[date[3:6]]), int(date[12:14])+9, int(date[15:17]), int(date[18:])
if (hour>24):
    hour -=hour
print(f'최초 로그인 시간 : {mon}월 {day}일 {hour}시 {min}분 {sec}초')

while progress == 0 :
    if (mon==target_mon) and (day==target_day) and (hour==target_hour) and (min==target_min) and (sec==target_sec) :
        time.sleep(0.5)
        driver.refresh()
        driver.implicitly_wait(60)      ##페이지 새로고침 후 최대 60초까지 대기
        try:
            ## 예매하기 버튼 클릭
            driver.find_element(By.LINK_TEXT,"예매하기").click()
            ## 예매 버튼 클릭 시간 확인
            date = urllib.request.urlopen(url).headers['Date'][5:-4]
            day, mon, hour, min, sec = int(date[:2]), int(month[date[3:6]]), int(date[12:14])+9, int(date[15:17]), int(date[18:])
            if (hour>24):
                hour -=hour
            print(f'클릭시간 : {mon}월 {day}일 {hour}시 {min}분 {sec}초')
            progress = 1
        except:
            pass
    else:
        date = urllib.request.urlopen(url).headers['Date'][5:-4]
        day, mon, hour, min, sec = int(date[:2]), int(month[date[3:6]]), int(date[12:14])+9, int(date[15:17]), int(date[18:])
        if (hour>24):
            hour -=hour
        time.sleep(0.5)
        print(f'현재 [{url}]의 서버시간 {mon}월 {day}일 {hour}시 {min}분 {sec}초')

while(True):
    pass


## 수정 필요 사항

# 1. Selenium 드라이버 업데이트로 인한 명령 변경 (이전에 있던것도 수정 필요)
# 2. 다중 접속 및 시간 지연에 대한 처리 보완 (59.6~60.0초 시 티켓팅 가능하도록)
# 3. 자동완성으로 인한 로그인 불가 문제 발생 (시간을 두고 키면 문제 발생 안하는듯..)
# 4. 시간 차를 두고 여러 개의 프로그램이 한꺼번에 돌아가도록 세팅