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

class QqEmail:
	try:
		#参数的定位
		path=os.getcwd()
		file=open(CONFIG_FILE, "r",encoding= "utf-8")
		data=yaml.load(file)
		random_date=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
		url=data['qqemail'].get('url')
		name=data['qqemail'].get('name')
		password=data['qqemail'].get('password')
		driver = webdriver.Chrome()
		# driver.maximize_window()
		driver.get(url)
		wait=WebDriverWait(driver,10)
	except Exception as msg1:
		print(msg1)
		print("参数定位错误")
		# return "False"	
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
					if("邮件/QQ邮箱[浏览]" in text):
						print('封堵成功')
						return "True"

				except Exception as msg:
					print(msg)
					print('封堵失败,网络异常')
					return "False"
	#登录
	def login(self):
		self.wait.until(EC.frame_to_be_available_and_switch_to_it('login_frame'))
		self.driver.find_element_by_name("u").clear()
		self.driver.find_element_by_name("u").send_keys(self.name)
		self.driver.find_element_by_name("p").clear()
		self.driver.find_element_by_name("p").send_keys(self.password)
		self.driver.find_element_by_id("login_button").click()
		self.driver.switch_to_default_content()
	#写信
	def sendmessage(self):
		# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#composebtn')))
		time.sleep(5)
		self.driver.find_element_by_link_text('写信').click()
		self.wait.until(EC.frame_to_be_available_and_switch_to_it('mainFrame'))
		# driver.find_element_by_xpath("//*[@id='toAreaCtrl']/div[2]/input").send_keys('aa_xiawei@163.com')
		self.wait.until(EC.presence_of_element_located((By.XPATH,".//*[@id='toAreaCtrl']/div[2]/input"))).send_keys('aa_xiawei@163.com')
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#subject'))).send_keys('friends'+self.random_date)
		self.driver.switch_to_frame(self.driver.find_element_by_tag_name('iframe'))
		self.driver.find_element_by_tag_name('body').send_keys('text'+self.random_date)
		self.driver.switch_to.parent_frame()
		time.sleep(5)

		#添加附件
		if (sys.argv[1] == "upload"):
			self.upload()
		#点击发送
		self.driver.find_element_by_link_text('发送').click()
		time.sleep(5)
		#断言邮件是否发送成功
		try:
			#定位发送成功标识
			text=self.wait.until(EC.presence_of_element_located((By.ID,'sendinfomsg'))).get_attribute('textContent')
			print(text)
			if("已发送" in text):#标识发送成功
				print('封堵失败，发送成功')
				return "False"

		except TimeoutException as msg:#无发送成功的标识
			print(msg)
			print('封堵成功')
			return "True"
	#添加附件
	def upload(self):
		self.driver.find_element_by_xpath("//input[contains(@name,'UploadFile')]").send_keys(DATA_PATH+'\\qq_text.txt')







if __name__ == '__main__':
	qqEmail = QqEmail()
	qqEmail.action()