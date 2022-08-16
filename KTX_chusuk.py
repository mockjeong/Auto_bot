import warnings
import selenium
warnings.filterwarnings(action='ignore')
from selenium import webdriver
import time

import urllib.request
month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

    
## 로그인 ID/PW 기록 (일단 내 아이디)
login_id = '0960000414'
login_pw = 'dbwjdahr11!'

## Chrome Driver 경로 지정
driverPath = r"chromedriver.exe" 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(driverPath, options=options)
# dmriver.set_window_size(1920, 1080)
driver.implicitly_wait(4)

## 코레일 추석 예매 표 사이트 접속
driver.get('https://www.letskorail.com/?NaPm=ct%3Dl6uogvkp%7Cci%3Dcheckout%7Ctr%3Dds%7Ctrx%3D%7Chk%3Df13fbc87f23e83e678fe5db411a12e10e3442720') 
driver.implicitly_wait(10)
driver.find_element("xpath","/html/body/div[1]/div/input").click()

## 최초 로그인 시간 확인
url = 'https://www.letskorail.com/'
date = urllib.request.urlopen(url).headers['Date'][5:-4]
day, mon, hour, min, sec = int(date[:2]), int(month[date[3:6]]), int(date[12:14])+9, int(date[15:17]), int(date[18:])
if (hour>24):
    hour -=hour
print(f'최초 로그인 시간 : {mon}월 {day}일 {hour}시 {min}분 {sec}초')

target_mon = 8
target_day = 16
target_hour = 21
target_min = 40
target_sec = 59
progress = 0

print(f'{target_mon}월 {target_day}일 {target_hour}시 {target_min}분 {target_sec}초에 예약을 시도합니다.')


while progress == 0 :
    if (mon==target_mon) and (day==target_day) and (hour==target_hour) and (min==target_min) and (sec==target_sec) :
        time.sleep(0.5)
        try:
            driver.find_element("xpath","/html/body/div[2]/div[2]/div/div[2]/div[1]/a").click()
            driver.implicitly_wait(2)      ##페이지 새로고침 후 최대 60초까지 대기

            #id, 비밀번호 입력
            driver.find_element("name",'txtMemberNo').send_keys(login_id)
            driver.find_element("name",'txtPwd').send_keys(login_pw)
            driver.find_element("xpath","/html/body/div/div/div/div[2]/div[1]/form/a").click()
            ## 예매 버튼 클릭 시간 확인
            date = urllib.request.urlopen(url).headers['Date'][5:-4]
            day, mon, hour, min, sec = int(date[:2]), int(month[date[3:6]]), int(date[12:14])+9, int(date[15:17]), int(date[18:])
            if (hour>24):
                hour -=hour
            print(f'클릭시간 : {mon}월 {day}일 {hour}시 {min}분 {sec}초')
            progress = 1
            driver.implicitly_wait(1)      ##페이지 새로고침 후 최대 60초까지 대기
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


