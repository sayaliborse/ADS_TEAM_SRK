
# coding: utf-8

# In[12]:


# coding: utf-8

# In[207]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import tabulate
import sys
import urllib.request
import os
import shutil
import logging
import zipfile
import logging # for logging
import glob
import boto.s3
from boto.s3.key import Key
import time
import datetime


logger= logging.getLogger()
logger.setLevel(logging.DEBUG)

#fh is file header
fh = logging.FileHandler('Problem1_log.log') #output the logs to a file
fh.setLevel(logging.DEBUG) #setting loglevel to DEBUG
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') #format for the output
fh.setFormatter(formatter)
logger.addHandler(fh)

#ch is console header
ch = logging.StreamHandler(sys.stdout ) #print the logs in console as well
ch.setLevel(logging.DEBUG) #setting loglevel to DEBUG
formatter = logging.Formatter('%(levelname)s - %(message)s') #format for the output
ch.setFormatter(formatter)
logger.addHandler(ch)


# In[ ]:


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
        cik = str(sys.argv[1])
        year= str(sys.argv[2])
        docnumber = str(sys.argv[3])
        logging.info("URL for the 10-q file for CIK = %s and Accession_no = %s is created", cik, docnumber)
        zero_cik = calc_cik(cik)
        year = year[-2:]
        website = "https://www.sec.gov/Archives/edgar/data/" + cik+"/" + zero_cik+""+year[-2:]+docnumber +"/" + zero_cik+ "-" + year[-2:]+"-" +docnumber+"-index.htm"
        try:
            r = requests.head(website)
            
            # prints the int of the status code. Find more at httpstatusrappers.com :)
        except requests.ConnectionError:
            print("Sorry you got Bad Internet. Let's try this again at a later time")
            
        
        if(r.status_code == 200):
            print("Website Accessed")
            logging.info("Link is generated")
            
            condition = False
        else:
            print("Failed to connect basis data provide, kindly re-enter correct details")
            logging.info("Wrong input for CIK and Docnumber")

    return website


# In[182]:


def scrape(website):
    res = requests.get(website)
    soup = BeautifulSoup(res.content,'lxml')
    #tables = soup.find('table')
    tbl = soup.findAll('table')
    print(len(tbl))

    for table in tbl:
        for tr in table.findAll('tr'):
            for td in tr.findAll('td')[2:4]:
                filing_type = td.string
                if filing_type=='10-Q':
                    gen_links = [a['href'] for a in tr.findAll('a')]
                    print('generated-link is:   ',gen_links)
                    for links in gen_links:
                        web_link = 'https://www.sec.gov' + links
                        print('web-link is:   ',web_link)
                        logging.info("10 Link generated")
                        
    tablelist = []

    soup = BeautifulSoup((urllib.request.urlopen(web_link)),"html.parser")
    tables = soup.find_all('table')
    for table in tables: 
        for tr in table.find_all('tr'):
            i = 0
            for td in tr.findChildren('td'):
                if ("background" in str(td.get('style'))):
                    tablelist.append(table)
                    i = 1
                    break
            if(i == 1):
                break
    return tablelist            


# In[208]:


def generate_csv(tablelist):
    destination = 'all_csv'
    print('length of table in generate_csv is:',len(tablelist))
    i = 1
    for new_tab in tablelist:
        df = pd.read_html(str(new_tab))
        file_name = 'my_data'+str(i)+ '.csv'
        
        df[0].to_csv(os.path.join(destination,file_name))
        i = i + 1 
        
    print('CSV Generated and Zip created')
    shutil.make_archive(r'zip_all_csv', 'zip', r'all_csv')
    logging.info("CSV has been made and Zipped")
    return



x = 'all_csv'
if not os.path.exists(x):
    os.makedirs(x)
logging.info("Directory Created")

website = start()
tablelist = scrape(website)
generate_csv(tablelist)


# In[13]:




AWS_ACCESS_KEY_ID = str(sys.argv[4])
AWS_SECRET_ACCESS_KEY = str(sys.argv[5])

try:
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY)

    print("Connected to S3")

except:
    logging.info("Amazon keys are invalid!!")
    print("Amazon keys are invalid!!")
    exit()


ts = time.time()
st = datetime.datetime.fromtimestamp(ts)    
bucket_name = AWS_ACCESS_KEY_ID.lower()+str(st).replace(" ", "").replace("-", "").replace(":","").replace(".","")
bucket = conn.create_bucket(bucket_name)
print("bucket created")
zipfile = 'all_csv.zip'
print ("Uploading %s to Amazon S3 bucket %s", zipfile, bucket_name)
    
def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()
    
k = Key(bucket)
k.key = 'all_csv'
k.set_contents_from_filename(zipfile,
cb=percent_cb, num_cb=10)
print("Zip File successfully uploaded to S3")

