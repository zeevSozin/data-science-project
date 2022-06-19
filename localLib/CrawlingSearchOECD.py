#!/usr/bin/env python
# coding: utf-8

# # Importing libraries including:
# -pandas: storing data
# -os: path browsing in OS
# -time: for delaying and timing quaries
# -selenium: crawling,get requests, entering keys and scraping webpage elements

# In[1]:


import pandas as pd
import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


chrome_options=Options()
chrome_options.add_argument("--incognito")
chrome_service=Service(ChromeDriverManager().install())


# # Sub functions:

# In[3]:


def get_OECD_Main_page():
    Main_page=webdriver.Chrome(options=chrome_options,service=chrome_service)
    base_url="https://www.oecd-ilibrary.org/"
    Main_page.get(base_url)
    return Main_page


# In[4]:


def free_search_in_OECD_ilibrary(search_phrase,page):
    search_element=page.find_element(By.XPATH, '//*[@id="quickSearchBox"]')
    search_element.clear()
    search_element.send_keys(search_phrase)
    search_element.send_keys(Keys.RETURN)


# In[5]:


def latest_publication_year_search_result(page):
    publication_list_div=page.find_element(By.CLASS_NAME,'facetpub_year_facet')
    publication_list=publication_list_div.find_element(By.CLASS_NAME,'list-unstyled')
    listLen=publication_list.get_property('childElementCount')
    elementList = list()
    textList = list()
    if (listLen==1):
        publication_list = publication_list_div.find_element(By.TAG_NAME, 'li')
    else:
        publication_list=publication_list_div.find_elements(By.TAG_NAME, 'li')
        
    if (listLen==1):
        t = publication_list.text
        textList.append(t)
        elementList.append(publication_list)

    else:
        for elem in publication_list:
            t=elem.text
            textList.append(t)
            elementList.append(elem)

    elemnt_to_text_table=pd.DataFrame({"element":elementList,"Text":textList})
    elemnt_to_text_table=elemnt_to_text_table.sort_values(by='Text',ascending=False, na_position='last')
    if(listLen==1):
        elem=elemnt_to_text_table.iat[0,0]
        txt=elemnt_to_text_table.iat[0,1]
    else:
        elem=elemnt_to_text_table.iat[1,0]
        txt=elemnt_to_text_table.iat[1,1]
    return elem , txt
  
    


# In[6]:


def get_href_from_element(element):
    ref=element.find_element(By.TAG_NAME,"a")
    return ref.get_property('href')
    


# In[7]:


def get_url_after_search(page):
    Table_element=page.find_element(By.XPATH,'//*[@id="listItems"]/div[1]/div[1]')
    visable_title=Table_element.find_element(By.CLASS_NAME,"title_box")
    text=visable_title.text
    title=visable_title.find_element(By.TAG_NAME,"a")
    table_url=title.get_property('href')
    return table_url,text
    


# In[8]:


def get_url_from_search_result_page(page):
    element=page.find_element(By.CLASS_NAME,'post-glimps')
    element_ul=element.find_element(By.CLASS_NAME,'identifiers')
    element_url=get_href_from_element(element_ul)
    return element_url


# In[9]:


def get_Main_data_set_page(search_phrase,Data_main_page):
    category_list=list()
    link_list=list()
    related_items_section=Data_main_page.find_element(By.CLASS_NAME,'list-related-titles')
    related_items_list=related_items_section.find_elements(By.CLASS_NAME,'panel')
    flag=False
    substring="outlook"
    for item in related_items_list:
        name_p=item.find_element(By.CLASS_NAME,'intro-item')
        name=name_p.text
        if substring in name:
            break
        else:
            category_list.append(name)
        try:
            url_item=item.find_element(By.CLASS_NAME,'action-data-2')
            url=url_item.get_property('href')
        except NoSuchElementException:
            pass
        link_list.append(url)
        if search_phrase in name:
            flag=True
            Url_link=link_list[-1]
    res_table=pd.DataFrame({"Datasets":category_list,"URL":link_list})
    if (flag):
        print ("The Phrase is found")
        print ("Heare are another options of Datasets:")
        print (res_table.head(10))
        return Url_link
    else:
        print ("The search phrase:"+search_phrase+" didn't mathed please see other options of Datasets:")
        print (res_table.head(10))
        return -1


# ## Main fuction: Recives search key word and returns URL to dataset

# In[10]:


def Search_latest_dataset_link_on_OECD_Main_website(search_phrase): 
    Main_page=get_OECD_Main_page()
    
    #search_phrase="Road accidents"   #if you are calling this function plase commet out this line
    free_search_in_OECD_ilibrary(search_phrase,Main_page)
    time.sleep(4)         #sleep for 4 seconds before takin an action in order to load the page
    
    elem,txt=latest_publication_year_search_result(Main_page)
    print("The latest publicated year is:"+txt)
    
    sub_url=get_href_from_element(elem)
    
    search_page=webdriver.Chrome(options=chrome_options,service=chrome_service)
    search_page.get(sub_url)
    
    sub_url_1,title=get_url_after_search(search_page)
    print ("The title of the reaserch is:\n"+title)
    
    search_result_page=webdriver.Chrome(options=chrome_options,service=chrome_service)
    search_result_page.get(sub_url_1)
    
    Data_main_page_url=get_url_from_search_result_page(search_result_page)
    
    Data_main_page=webdriver.Chrome(options=chrome_options,service=chrome_service)
    Data_main_page.get(Data_main_page_url)
    
    Dataset_portal_link=get_Main_data_set_page(search_phrase,Data_main_page)
    
    Main_page.close()
    search_page.close()
    search_result_page.close()
    Data_main_page.close()
    
    return Dataset_portal_link


# ### This section calling the main function

# In[11]:

def GetDatasetUrl(args):
    URL=Search_latest_dataset_link_on_OECD_Main_website(args)
    print("The URl of the dataset is:\n"+URL)
    return URL


# ## This section below is the function above braked into sub_functions made for testing and maitain the code
# 

# In[12]:


#Main_page=get_OECD_Main_page()


# In[13]:


# search_phrase="Road accidents"
# free_search_in_OECD_ilibrary(search_phrase,Main_page)
# time.sleep(4)         #sleep for 4 seconds before takin an action in order to load the page


# In[14]:


# elem,txt=latest_publication_year_search_result(Main_page)
# print("The latest publicated year is:"+txt)


# In[15]:


#sub_url=get_href_from_element(elem)


# In[16]:


# search_page=webdriver.Chrome(options=chrome_options,service=chrome_service)
# search_page.get(sub_url)


# In[17]:


# sub_url_1,title=get_url_after_search(search_page)
# print ("The title of the reaserch is:\n"+title)


# In[18]:


# search_result_page=webdriver.Chrome(options=chrome_options,service=chrome_service)
# search_result_page.get(sub_url_1)


# In[19]:


#Data_main_page_url=get_url_from_search_result_page(search_result_page)


# In[20]:


# Data_main_page=webdriver.Chrome(options=chrome_options,service=chrome_service)
# Data_main_page.get(Data_main_page_url)


# In[21]:


#Dataset_portal_link=get_Main_data_set_page(search_phrase,Data_main_page)


# In[22]:


#print (Dataset_portal_link)


# In[23]:


# Main_page.close()
# search_page.close()
# search_result_page.close()
#Data_main_page.close()

