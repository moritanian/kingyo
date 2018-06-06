# -*- coding: utf-8 -*-

from selenium import webdriver
import time

if __name__ == '__main__':
	url = "http://localhost/kingyo/webrtc/multi.html"
	driver = webdriver.Chrome("./../chromedriver/chromedriver.exe")
	driver.get(url)

	time.sleep(5)
	#driver.quit()