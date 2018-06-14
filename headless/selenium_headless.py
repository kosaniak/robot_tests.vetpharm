import selenium.webdriver


options = selenium.webdriver.FirefoxOptions()
options.set_headless()
wd = selenium.webdriver.firefox.webdriver.WebDriver(options=options)
wd.get('https://quintagroup.com/')
wd.get_screenshot_as_file('qg.png')
wd.close()
