# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 15:38:00 2021

@author: amanullah.awan
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time 
import pandas as pd

class TravelState:
    #Starting url
    start_url = "https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages.html"
    driver = None
    
    #Driver path
    CHROME_PATH = r'SeleniumDrivers/chromedriver.exe'
    
    #Request Function
    def start_request(self):
        self.driver = webdriver.Chrome(executable_path=self.CHROME_PATH)
        self.driver.get(self.start_url)
        
    #Parsing Function
    def parse(self):
        country_urls = self.driver.find_elements_by_css_selector("div[class='list parbase section'] > ul.default > li > p > a")
        self.data = []
        
        #Iterate over Country Urls
        for country in self.get_urls(country_urls):
            print(f"Now requesting to: {country}")
            
            #Get Country Urls
            self.driver.get(country)
            time.sleep(5)
            
            #Export items
            items = self.export_items(country)
            print(items)
            self.data.append(items)
                        
        return country
    
    #Exporting Items Function
    def export_items(self , url):
        #Get Country's Name 
        name = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-display-page-header > div > div.tsg-rwd-csi-contry-name').text    
        #Get Travel Advisory Level Data
        level = self.driver.find_element_by_css_selector('#tsg-rwd-advisories > div > a > h3.tsg-rwd-eab-title-frame').text
        #Get Date 
        date = self.driver.find_element_by_css_selector('#tsg-rwd-advisories > div > a > h3.tsg-rwd-eab-type-main-frame > div.tsg-rwd-eab-date-frame').text
        
        self.driver.find_element_by_css_selector("#csi-mainbody > div > div.tsg-rwd-csi-travel-advisories > div > div.tsg-rwd-alert-more-box > a.tsg-rwd-alert-more-box-btn").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div.tsg-rwd-accordion-nav-frame-for-freestanding-all-buttons-csi-show > a.set_1_button.hideThis.tsg-rwd-accordion-All-control-tsg_rwd_show_all_button').click()
        time.sleep(3)
        
        #Get Embassies Data
        emb = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div:nth-child(3)').text
        #Get Description Data
        description = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-travel-advisories > div > div.tsg-rwd-alert-more-box > div.tsg-rwd-alert-more-box-content').text
        #Get Facts Data
        facts = self.driver.find_element_by_css_selector("#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div.tsg-rwd-sidebar-qf-csi-show").text
        #Get Destination Data
        destination = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div:nth-child(4)').text
        #Get Entry Data
        entry = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div:nth-child(5)').text
        #Get Safety Data
        safety = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div:nth-child(6)').text
        #Get Law Data
        law = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div:nth-child(7)').text
        #Get Health Data
        health = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div:nth-child(8)').text
        #Get Travel Data
        travel = self.driver.find_element_by_css_selector('#csi-mainbody > div > div.tsg-rwd-csi-hide-show-maincontent-csi-show > div > div:nth-child(9)').text
        print("Now Writing")
        
        #Return Dictionary for above Data
        return {'Country-Name' : name , 
                'Travel-Advisory-Level' : level , 
                'Date' : date  , 
                'Description' : description ,
                'Facts' : facts ,
                'Embassy Data' : emb ,
                'Destination Data' : destination , 
                'Entry Data' : entry , 
                'Safety Data' : safety ,
                'Local Law' : law , 
                'Health Data' : health , 
                'Travel Data' : travel
                }
    
 
    #Function to return Urls in list.
    def get_urls(self , obj_list):
        return [url.get_attribute("href") for url in obj_list]
    
#main()Starts Here:

#Make Travel Class Object    
x = TravelState()

#Call the Required Methods
x.start_request()
x.parse()

#Export Data to Csv 
data_pd = pd.DataFrame.from_records(x.data)
data_pd.to_csv('travelscraped_data.csv', index=False)





        




          