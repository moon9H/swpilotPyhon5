# 과정 5 - (문제8) "로그인을 넘어"

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# 네이버 로그인 시 자동입력방지가 뜨지 않도록 하기 위해 사용하는 라이브러리들
import pyautogui
import pyperclip
import time

def bootChromeDriverandNaver() :
    options = Options()
    options.add_experimental_option('detach', True)  # 브라우저 바로 닫힘 방지
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 불필요한 메시지 제거

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://naver.com')

    return driver

def naverLogin(driver, naver_id, naver_pw) :
    # login 창으로 이동
    login_tab = driver.find_element(By.CSS_SELECTOR, 'a.MyView-module__link_login___HpHMW')
    login_tab.click()

    # id 입력창
    id = driver.find_element(By.CSS_SELECTOR, '#id')
    id.click()
    pyperclip.copy(naver_id)
    pyautogui.keyDown("command")
    pyautogui.press("v")
    pyautogui.keyUp("command")
    time.sleep(2)

    # 비밀번호 입력창
    pw = driver.find_element(By.CSS_SELECTOR, '#pw')
    pw.click()
    pyperclip.copy(naver_pw)
    pyautogui.keyDown("command")
    pyautogui.press("v")
    pyautogui.keyUp("command")
    time.sleep(1)

    # login 버튼
    btn_login  = driver.find_element(By.CSS_SELECTOR, '#log\.login')
    btn_login.click()

    return driver

def crawlNaver(driver):
    # 특정 요소가 로드될 때까지 대기
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#newsstand .MediaView-module__media_area___Z4js3')))
    
    # 페이지가 완전히 로드된 후 약간의 추가 대기
    time.sleep(2)
    
    # 특정 클래스의 img 태그 선택
    elements = driver.find_elements(By.CSS_SELECTOR, '#newsstand .MediaView-module__media_area___Z4js3 .MediaSubscriptionView-module__subscription_group___peb21 .MediaSubscriptionView-module__news_thumb___IA4y2 img')
    
    # 각 img 태그의 alt 속성 값을 추출
    news_titles = [element.get_attribute('alt') for element in elements]
    
    # 추출된 텍스트 출력
    for title in news_titles:
        print(title)

# [보너스 과제] - naverMail 목록 크롤링
def checkNaverMail(driver) :
    driver.get('https://mail.naver.com/v2/folders/0/all')

    # 메일 목록이 완전히 로드될 때 까지 대기
    wait = WebDriverWait(driver, 10)
    wait.until((EC.presence_of_element_located((By.CSS_SELECTOR, 'a.mail_title_link > span.text'))))

    # 보낸 사람 크롤링
    sender_list = driver.find_elements(By.CSS_SELECTOR, 'div.mail_sender > button')
    # 메일 목록 크롤링
    
    mail_list = driver.find_elements(By.CSS_SELECTOR, 'a.mail_title_link > span.text')

    for i in range(len(mail_list)) :
        clean_sender = sender_list[i].text.replace('\n', ' ')
        print(f"{clean_sender} : {mail_list[i].text}")
    

if __name__ == '__main__' :
    naver_id = input('Enter Your Naver ID: ').strip()
    naver_pw = input('Enter Your Naver PW: ').strip()
    chromeDriver = bootChromeDriverandNaver()
    print(naver_id, naver_pw)
    print('로그인 이전 추천 언론사')
    crawlNaver(chromeDriver, naver_id, naver_pw)
    naverLogin(chromeDriver)
    print('\n로그인 이후 추천 언론사')
    crawlNaver(chromeDriver)
    print('\n메일 목록')
    checkNaverMail(chromeDriver)