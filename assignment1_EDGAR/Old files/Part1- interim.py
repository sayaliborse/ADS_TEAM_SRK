
# coding: utf-8

# # Import libraries

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import tabulate
import sys


# # Importing CSV Data

# In[2]:


#allCik = pd.read_csv("C:\Users\rishi\Desktop\ADS_TEAM_SRK\assignment1_EDGAR\ALL_CIK.csv", low_memory= False)


# # Check for valid CIK

# In[6]:


#function to check if entered CIK is valid

#def CheckandAcceptCIK(num):
    #flag = False
    #for i in allCik["CIK"]:
        #if (num == i):
            #flag = True
            
    #if(flag == False):
        #print("Invalid CIK. Please run the program again")
        
        
    #else:
        #return str(num)
        


# # Add Leading Zeros

# In[5]:


#function to add leading zeroes 


def calc_cik(cik):

    cik_str = str(cik)
    length_cik = len(cik_str)
    final_length = 10 - length_cik
    i=0
    while i < final_length:
        cik_str ='0' + cik_str
        i= i+1
        
    return cik_str


# # Calculate Financial Year Part

# In[5]:


#function to calculate financial year part which is added to our link
# # Generating the URL

# In[7]:

def start():
    condition = True
    while(condition == True):
        cik = '1288776'
        year= '2015'
        docnumber ='000046'
        
        zero_cik = calc_cik(cik)
        year = year[-2:]
        website = "https://www.sec.gov/Archives/edgar/data/" + cik+"/" + zero_cik+""+year[-2:]+docnumber +"/" + zero_cik+ "-" + year[-2:]+"-" +docnumber+"-index.htm"
        print(website)
        try:
            r = requests.head(website)
            
            # prints the int of the status code. Find more at httpstatusrappers.com :)
        except requests.ConnectionError:
            print("Sorry you got Bad Internet. Let's try this again at a later time")
        
        if(r.status_code == 200):
            print("Website Accessed")
            condition = False
        else:
            print("Failed to connect basis data provide, kindly re-enter correct details")    
    
# In[15]:


        res = requests.get(website)
        soup = BeautifulSoup(res.content,'lxml')
    #table = soup.find_all('table')[0]
    #df = pd.read_html(str(table))
    #df[0].to_csv('my_data.csv')
        tables = soup.find_all('table')
        i = 1
    #len(tables)
        for table in tables:
            df = pd.read_html(str(table))
            df[0].to_csv('my_data'+ str(i) + '.csv')
            i = i + 1

        res = requests.get(website)
        soup = BeautifulSoup(res.content,'lxml')
    #tables = soup.find('table')
        tbl = soup.findAll('table')


# In[19]:


        for table in tbl:
            for tr in table.findAll('tr'):
                for td in tr.findAll('td')[:2]:
                    filing_type = td.string
                    if filing_type=='10-Q':
                        gen_links = [a['href'] for a in tr.findAll('a')]
                        print('generated-link is:   ',gen_links)
                        for links in gen_links:
                            web_link = 'https://www.sec.gov' + links
                            print('web-link is:   ',web_link)
                            res_new = requests.get(web_link)
                            soup_new = BeautifulSoup(res_new.content,'lxml')
                            tables_new = soup_new.find_all('table', attrs={'border':"1", 'cellpadding':"0", 'cellspacing':"0", 'style':"border:none;border-collapse:collapse;width:100%;"})
                            i = 1
                        #print('length of table is:',len(tables_new)) 
                            for new_tab in tables_new:
                                df = pd.read_html(str(new_tab))
                                df[0].to_csv('my_data'+ str(i) + '.csv')
                                i = i + 1
                                print("Successful")
    

