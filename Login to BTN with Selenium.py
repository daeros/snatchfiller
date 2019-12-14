
driver = webdriver.Firefox()
driver.get('https://broadcasthe.net/login.php')

username = input('username?')
password = input('password?')

elem = driver.find_element_by_css_selector('#username')
elem.click()
elem.send_keys(username)
elem2 = driver.find_element_by_css_selector('#password')
elem2.click()
elem2.send_keys(password)
login = driver.find_element_by_css_selector('.submit')
login.click()
