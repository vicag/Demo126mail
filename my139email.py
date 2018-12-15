#!/usr/bin/env Python
#coding = utf-8
 
from selenium import webdriver
import yaml
import os,sys,time
from os import path
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import string,random
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from configs.config import CONFIG_FILE,DATA_PATH

class My139Email:
	#定义参数
	try:
		file=open(CONFIG_FILE, "r",encoding= "utf-8")
		data=yaml.load(file)
		random_date=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
		url=data['my139email'].get('url')
		name=data['my139email'].get('name')
		password=data['my139email'].get('password')
		driver = webdriver.Chrome()
		wait = WebDriverWait(driver,30)
		# driver.maximize_window()
		driver.get(url)
	except Exception as msg1:
		print(msg1)
		print("参数定位错误")
	else:	
		def action(self):
			try:				
				#登录
				self.login()
				#发送邮件
				self.sendmessage()

			# 断言封堵
			except TimeoutException:
				time.sleep(5)
				try:
					text = self.driver.find_element_by_id('strType').get_attribute('textContent')  
					print(text)
					if("邮件/网易邮箱[浏览]" in text):
						print('封堵成功')
						return "True"

				except Exception as msg:
					print(msg)
					print('封堵失败,网络异常')
					return "False"
	# 登录
	def login(self):
		self.wait.until(EC.presence_of_element_located((By.NAME,'UserName'))).clear()
		self.driver.find_element_by_name('UserName').send_keys(self.name)
		self.driver.find_element_by_name("Password").clear()
		self.driver.find_element_by_name("Password").send_keys(self.password)
		self.driver.find_element_by_id("loginBtn").click()
	#写信
	def sendmessage(self):
		self.wait.until(EC.frame_to_be_available_and_switch_to_it('welcome'))
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.i_iconWrite'))).click()#点击写信
		self.driver.switch_to_default_content()
		self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[contains(@id,'compose_')]")))
		self.driver.maximize_window()
		time.sleep(3)
		self.driver.find_element_by_xpath("//*[@class='addrText-input'and @type = 'text' and @tabindex = '1']").send_keys('275023669@qq.com')#添加收件人
		# driver.find_element_by_id('txtSubject').send_keys('friends'+random_date)#添加主题
		time.sleep(3)
		self.driver.find_element_by_xpath("//*[@id='txtSubject' and @name='txtSubject']").send_keys('friends'+self.random_date)#添加主题
		#添加附件
		time.sleep(3)
		if (sys.argv[1] == "upload"):
			self.upload()

		time.sleep(5)
		self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@hidefocus,'1')]"))#切换到没有id和name的frame中去
		self.driver.find_element_by_tag_name('body').send_keys('test'+self.random_date)#添加正文
		self.driver.switch_to.parent_frame()#退出frame
		# driver.find_element_by_css_selector('.p_relative').click()#点击发送
		self.driver.find_element_by_xpath("//*[@id=\"topSend\"]/span").click()
		time.sleep(5)
		try:
			text=self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='snedStatus']"))).get_attribute('textContent')
			# print('11111')
			print(text)
			if("已发送" in text):
				print('封堵失败，发送成功') 	
				return "False"


		except TimeoutException as msg:
			print('封堵成功,无发送成功标识')
			return "True"
	def upload(self):
		self.upload = self.driver.find_element_by_css_selector('#uploadInput')
		self.upload.send_keys(DATA_PATH+'\\my139email_test.txt')
		time.sleep(5)
		try:
			text=self.driver.find_element_by_link_text('续传').get_attribute('textContent')
			print(text)
			if("续传"in text):
				print('封堵成功')
				return True
			else:
				print('封堵失败')
				return False

		except:
			print('封堵失败')
			return False





if __name__ == '__main__':
	my139Email = My139Email()
	my139Email.action()