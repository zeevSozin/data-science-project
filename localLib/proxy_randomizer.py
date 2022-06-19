#!/usr/bin/env python
# coding: utf-8

# In[13]:


import selenium
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# In[15]:


def getProxList():
    base_url='https://premproxy.com/list/ip-port/1.htm'
    chrome_options=Options()
    chrome_options.add_argument("--incognito")
    chrome_service=Service(ChromeDriverManager().install())
    Main_Page=webdriver.Chrome(options=chrome_options,service=chrome_service)
    Main_Page.get(base_url)
    time.sleep(3)
    Proxy_list=Main_Page.find_element(By.ID, 'ipportlist')
    proxy_ip_list=Proxy_list.find_elements(By.TAG_NAME,'li')
    proxy_ipAdress_list=list()
    for add in proxy_ip_list:
        proxy_ipAdress_list.append(add.text)
    return proxy_ipAdress_list

