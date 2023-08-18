from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


#Chrome 브라우저로 실행하라
driver = webdriver.Chrome()


#get() -> 페이지 이동
driver.get("http://www.python.org")
#요소중에 name의 속성값이 "q"인 것을 찾아라
#요소가 1개일 때 -> find_element / 요소가 1개 이상이라면 -> find_elements
elem = driver.find_element(By.NAME, "q")


#Input 태그의 입력란 초기화
elem.clear()
#send_keys->문자열 전달(입력), 명령 실행
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

#사용이 끝나면 close()로 종료
driver.close()