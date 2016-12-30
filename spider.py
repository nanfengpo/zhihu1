# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
import urllib


# ======打开PhantomJS浏览器======
#browser=webdriver.Chrome()
browser=webdriver.PhantomJS()

# ======================================================
# ========================1、登录=========================
# ======================================================
browser.get("https://www.zhihu.com/#signin")
#time.sleep(5)
account=browser.find_element_by_name('account')
account.send_keys("zhyeixlt56320152@163.com")
password=browser.find_element_by_name('password')
password.send_keys("qqxrwsx039")
#time.sleep(5)# 这里必须停留一段时间！！！知乎需要根据我们填写的内容来确定三种登录方式的哪一种
# ======登录界面的三种情况======
try:
    # 输入验证码登录的情况
    captcha=browser.find_element_by_xpath('//div[@class="view view-signin"]/form[1]/div[1]/div[3]/input[@id="captcha"]')
    print "======有验证码======"
    #captcha_url=browser.find_element_by_xpath('//div[@class="view view-signin"]/form[1]/div[1]/div[3]/div[1]/img[@class="js-refreshCaptcha captcha"]').get_attribute("src")
    #print "captcha_url:"+captcha_url
    # ======把验证码图片下载到本地======
    captcha_store="/home/nanfengpo/Documents/requests+bs4/zhihu1/captcha.png"

    # 方法1：通过截图
    browser.save_screenshot(captcha_store)

    '''
    # 方法2：用requests库下载图片(此方法不行)
    with open(captcha_store,'wb') as cpt:
        cpt.write(requests.get(captcha_url).content)
    '''
    '''
    # 方法3：用urllib库下载图片
    urllib.urlretrieve(captcha_url,captcha_store)
    '''
    captcha_text=raw_input("输入验证码:")
    captcha.send_keys(captcha_text)
    captcha.send_keys(Keys.RETURN)
# 手动点击倒立汉字登录的情况
except NoSuchElementException:
    try:
        captcha=browser.find_element_by_xpath('//div[@class="view view-signin"]/form[1]/div[1]/div[3]/div[@class="Captcha-operate"]')
        wait_manual_operation=raw_input("手动点击倒立汉字登录,完成后输入任意键继续：")
    # ======若没有验证码，直接回车======
    except NoSuchElementException:
        print "======没有验证码======"
        password.send_keys(Keys.RETURN)

print "======登录成功！======"

# ============================================================
# ========================2、打开知乎问题页面=======================
# ===========================================================

# 太快了，必须得等一下才能完全登录进去！！！
#browser.implicitly_wait(10) #操你妈，这个函数没个屁用
time.sleep(5)
'''
# 测试在新窗口打开是否保持登录状态：
js_newwindow='window.open("https://www.zhihu.com/question/27621722");'
browser.execute_script(js_newwindow)
handles=browser.window_handles
browser.switch_to.window(handles[-1])
time.sleep(5)# 打开新窗口后这个是必须的，否则可能无法输出title
'''
browser.get("https://www.zhihu.com/question/27621722")
# 看是否成功打开======
print browser.title

# 检查是否有“更多”按钮，若有，则持续点击，直到没有，使得所有回答都被加载======
'''
#loadmore = browser.find_element_by_xpath("//a[@class='zg-btn-white zu-button-more']")

loadmore=WebDriverWait(browser,10).until(
    EC.element_to_be_clickable((By.XPATH,"//a[@class='zg-btn-white zu-button-more']"))
)
loadmore=WebDriverWait(browser,10).until(
    EC.presence_of_element_located((By.XPATH,"//a[@class='zg-btn-white zu-button-more']"))
)
print loadmore.text #“更多”
loadmore.click()
print loadmore.text #“加载中”

'''
start=time.clock()
while 1:
    try:
        '''
        loadmore=WebDriverWait(browser,20).until(
            EC.presence_of_element_located((By.XPATH,"//a[@class='zg-btn-white zu-button-more']"))
        )
        '''
        time.sleep(2)
        loadmore=WebDriverWait(browser,30).until(
            EC.element_to_be_clickable((By.XPATH,"//a[@class='zg-btn-white zu-button-more']"))
        )
        loadmore.click()
    except TimeoutException:
        end=time.clock()
        print "加载全部回答用时："+str(end-start)+"s"
        break

sites = browser.find_elements_by_xpath('//div[@class="zm-item-answer  zm-item-expanded"]')
# 点击“更多”之前有20个site，每点击一次就增加10个
print len(sites)
#print sites
s=0 # 被赞数大于100的回答的个数
for i in range(0,len(sites)):
    try:
        count=sites[i].find_element_by_xpath("div[1]/button[1]/span[1]")
        print count.text
        count_int=int(count.text)
        if count_int>100 :
            s=s+1
            link = sites[i].find_element_by_xpath('link')
            print link.get_attribute('href')
        else :
            pass
    except NoSuchElementException:
        print "not find answer"
print "共有"+str(s)+"个回答被赞数大于100"

w=raw_input("输入任意键结束：")
browser.close()
browser.quit()
