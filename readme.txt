【目的】
一个小小的测试
针对一个问题的页面（https://www.zhihu.com/question/27621722）
爬虫，找出被赞数大于100的回答的答主的信息。

【难点】
1、最准确的页面分析代码是把Elements的html下载后的代码！其他的都不准确！很多问题都是页面分析不够造成的，没有考虑到多发情况，例如知乎登录有三种情况：无验证码/英文验证码/倒立汉字验证码，要分析每种情况的页面的特点，从而针对每种页面分类处理。
2、善于利用try-except，实际上就是一种特殊的if-else，只不过把try里面的代码作为if的判断语句罢了！参考登录界面的三种情况
3、browser.implicitly_wait(10) #操你妈，这个函数没个屁用，直接用time.sleep()
4、【重要】先用谷歌浏览器操作（browser=webdriver.Chrome()）！原因如下：
- 有些问题可能需要手动操作（如倒立汉字选择）
- 有界面能更一目了然地发现问题。比如三种登录界面就是这样发现的，之前用PhantomJS我一直以为登录成功了，是不能click“更多”按钮导致出错，而实际上a标签也可以click，错误原因是我没考虑到还有倒立汉字登录方式，根本没登录进去，因此点击后就进入了提示登录框
5、注意点击按钮前一定要确保能点击（element_to_be_clickable），此时应当使用
loadmore=WebDriverWait(browser,10).until(
            EC.element_to_be_clickable((By.XPATH,"//a[@class='zg-btn-white zu-button-more']"))
)
6、while+try循环！！！
- 可以解决重复某一操作直到不能操作导致出错（except）为止
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

？7、输入账号密码后必须停留一段时间！！！知乎需要根据我们填写的内容来确定三种登录方式的哪一种
8、问题：谷歌和PhantomJS都不能下载验证码，保存下来的会与实际的不一致，因此只能手动输入
9、PhantomJS可以通过截图的方式保存验证码（ 谷歌浏览器不可以！没有save_screenshot这个函数）
captcha_store="/home/nanfengpo/Documents/requests+bs4/zhihu1/captcha.png"
browser.save_screenshot(captcha_store)
10、PhantomJS多页面：打开新窗口后必须等一会，否则可能无法立即获得title等信息
