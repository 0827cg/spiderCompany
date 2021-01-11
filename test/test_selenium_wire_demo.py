#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/31 11:28
"""

from seleniumwire import webdriver  # Import from seleniumwire


chrome_driver_path = "D:\\work\\python\\pycharm\\200506\\spiderCompany\\lib\\chromedriver_win32\\chromedriver.exe"

# Create a new instance of the Firefox driver
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Go to the Google home page
driver.get('http://www.baidu.com')

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(
            request.url,
            request.response.status_code,
            request.response.headers['Content-Type']
        )