import warnings
import selenium
warnings.filterwarnings(action='ignore')
from selenium import webdriver
import time

import urllib.request
month = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
    'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

## Chrome Driver 경로 지정
driverPath = r"chromedriver.exe" 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(driverPath, options=options)
driver.set_window_size(1920, 1080)
driver.implicitly_wait(4)

## 로그인 ID/PW 기록 (일단 내 아이디)
login_id = 'jeongmock'
login_pw = 'dbwjdahr11!'

## 서울시 공공예약 사이트 접속
driver.get('https://yeyak.seoul.go.kr/web/main.do') 
time.sleep(1)

##로그인 버튼 클릭
driver.find_element("xpath","/html/body/div/header/div[1]/div/div[1]/a").click()
time.sleep(1)
#ID/PW 입력 및 로그인
driver.find_element("name",'userid').send_keys(login_id)
driver.find_element("name",'userpwd').send_keys(login_pw)
driver.find_element("xpath","/html/body/div/div[3]/div[2]/div/div/div/div[1]/form/div[1]/button").click()
time.sleep(1)
##공간 시설 클릭
driver.find_element("xpath","/html/body/div[1]/header/div[2]/div[2]/nav/div/ul/li[2]/a/span").click()
time.sleep(1)
##캠핑장 클릭
driver.find_element("xpath","/html/body/div[1]/div[3]/div[2]/div/div[1]/div/a[2]").click()
time.sleep(1)
#ID/PW 입력 및 로그인
driver.find_element("name",'sch_text').send_keys('9월 난지 12')
driver.find_element("xpath","/html/body/div[1]/div[3]/div[2]/div/div[2]/form/fieldset/button[1]").click()
time.sleep(1)
##첫 번째 검색 결과 클릭
driver.find_element("xpath","/html/body/div[1]/div[3]/div[2]/div/div[3]/ul/li/a/div[2]/h4").click()
time.sleep(1)
##팝업 닫기 클릭
driver.find_element("xpath","/html/body/div/div[3]/div[2]/div/div[1]/div/div[2]/button/span").click()
time.sleep(1)

target_mon = 8
target_day = 16
target_hour = 13
target_min = 59
target_sec = 59
progress = 0

print(f'{target_mon}월 {target_day}일 {target_hour}시 {target_min}분 {target_sec}초에 예약을 시도합니다.')

## 최초 로그인 시간 확인
url = 'https://yeyak.seoul.go.kr/'
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
        driver.find_element("xpath","/html/body/div/div[3]/div[2]/div/div[1]/div/div[2]/button/span").click()
        try:
            ## 날짜 버튼 클릭 (수정 필요, 현재는 8월 16일)
            driver.find_element("xpath","/html/body/div/div[3]/div[2]/div/form[2]/div[1]/div[1]/div[2]/div/table/tbody/tr[3]/td[6]/a/span[1]").click()
            ## 예약하기 클릭
            res_but = "/html/body/div/div[3]/div[2]/div/form[2]/div[1]/div[2]/div/div/a[1]"
            if(driver.find_element("xpath",res_but).text=='예약하기'):
                driver.find_element("xpath",res_but).click()
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


