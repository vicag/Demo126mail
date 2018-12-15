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

class My126Email:
	try:
		#参数的定位
		path=os.getcwd()
		file=open(CONFIG_FILE, "r",encoding= "utf-8")
		data=yaml.load(file)
		random_date=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
		url=data['my126email'].get('url')
		name=data['my126email'].get('name')
		password=data['my126email'].get('password')
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
					if("邮件/网易邮箱[浏览]" in text):
						print('封堵成功')
						return "True"

				except Exception as msg:
					print(msg)
					print('封堵失败,网络异常')
					return "False"

	def login(self):
		self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//*[@class='loginUrs']/iframe")))#切入iframe
		self.driver.find_element_by_name("email").clear() #输入账户
		self.driver.find_element_by_name("email").send_keys(self.name)
		self.driver.find_element_by_name("password").clear()  #输入密码
		self.driver.find_element_by_name("password").send_keys(self.password)
		self.driver.find_element_by_id("dologin").click()  #登录按钮
		time.sleep(2)
		 
		self.driver.switch_to_default_content()#跳出frame，回到主页面
		 
		print(self.driver.title)#获取标题
	def sendmessage(self):
		self.wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='dvNavTop']/ul/li[2]/span[2]"))).click()#点击写信

		 
		self.driver.find_element_by_class_name('nui-editableAddr-ipt').send_keys('275023669@qq.com')#添加收件人
		 
		self.driver.find_element_by_xpath("//*[@class='nui-ipt-input'and @type = 'text' and @tabindex = '1']").send_keys('friends'+self.random_date)#添加主题

		if (sys.argv[1] == "upload"):
			self.uploadfujian()

		self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@class,'APP-editor-iframe')]"))#切换到没有id和name的frame中去
		self.driver.find_element_by_class_name("nui-scroll").send_keys('test'+self.random_date)#添加正文
		self.driver.switch_to_default_content()#退出frame
		self.driver.find_element_by_xpath("//*[@class='nui-toolbar-item']/div/span[2]").click()#点击发送
		time.sleep(10)
		# 断言邮件是否发送成功
		try:
			#定位发送成功标识
			text=self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='tK1' and @tabindex = '1']"))).get_attribute('textContent')
			print(text)
			if("成功" in text):#标识发送成功
				print('封堵失败，发送成功')
				return "False"

		except TimeoutException as msg:#无发送成功的标识
			print(msg)
			print('封堵成功')
			return "True"
	#添加附件
	def uploadfujian(self):
		upload = self.driver.find_element_by_class_name('O0')
		upload.send_keys(DATA_PATH+'\\my126email_test.txt')
		print(upload.get_attribute('value'))		





if __name__ == '__main__':
	my126Email = My126Email()
	my126Email.action()