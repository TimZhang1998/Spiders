from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--proxy-server=http://110.52.235.119:9999')  
driver = webdriver.Chrome(chrome_options=chromeOptions)

# 查看本机ip，查看代理是否起作用
driver.get("https://www.latlong.net")
print(driver.page_source)

# 退出，清除浏览器缓存
driver.quit()
