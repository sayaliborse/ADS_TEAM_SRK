#!/usr/bin/env python
# coding: utf-8

# In[4]:


import mechanicalsoup as ms
import pandas as pd
import numpy as np
import requests
import re
import os
import glob
import csv
import numpy as np
import matplotlib.pyplot as plt
import math
get_ipython().run_line_magic('matplotlib', 'inline')
import json
from bs4 import BeautifulSoup
import urllib.request as rq
import urllib
from zipfile import ZipFile
from io import BytesIO
import lxml
from sklearn import preprocessing


# In[2]:


def downloadhistoricaldata(trainQ, testQ, tables,session, flag):
    for link in tables:
        if(trainQ in link['href'] or testQ in link['href']):
            c = 'https://freddiemac.embs.com/FLoan/Data/' + link['href']
            response = session.get(c)
            z = ZipFile(BytesIO(response.content)) 
            z.extractall(os.getcwd())
            flag = 1
    return flag


# In[3]:


def login(username, password, qtrain, qtest):
    login = "borse.s@husky.neu.edu"
    password = "LD^M{LS4"
    trainQ = 'Q12005'
    testQ = 'Q22005'
    
    s = requests.Session()
    url = "https://freddiemac.embs.com/FLoan/secure/auth.php"
    url2 = "https://freddiemac.embs.com/FLoan/Data/download.php"
    browser = ms.Browser(session = s)
    print("Logging in....")
    login_page = browser.get(url)
    login_form = login_page.soup.find("form",{"class":"form"})
    login_form.find("input", {"name":"username"})["value"] = login
    login_form.find("input", {"name":"password"})["value"] = password
    response = browser.submit(login_form, login_page.url)
    login_page2 = browser.get(url2)
    print("To the continue page...")

    next_form = login_page2.soup.find("form",{"class":"fmform"})
    a= next_form.find("input",{"name": "accept"}).attrs
    a['checked']=True

    response2 = browser.submit(next_form, login_page2.url)
    print("Start Downloading from..."+ response2.url)
    table = response2.soup.find("table",{"class":"table1"})
    
    t = table.find_all('a')
    flag = 0
    flag = downloadhistoricaldata(trainQ, testQ, t,s, flag) 

    if flag == 1:
        print("Data downloaded successfully!!")
    else:
        print("Error in downloading data")


# In[21]:


def downloaddataincsv(trainQ, testQ):
    trainfile = "historical_data1_time_"+ trainQ + ".txt"
    testfile = "historical_data1_time_"+ testQ + ".txt"
    f1 = "train_" + trainQ + ".csv"
    f2 = "test_" + testQ + ".csv"
    with open(f1, 'w',encoding='utf-8') as file: 
        df = pd.read_csv(trainfile ,delimiter ="|", names=['credit_score','first_payment_date','fthb_flag','matr_date','msa',"mortage_insurance_pct",'no_of_units','occupancy_status','cltv','dti_ratio','original_upb','original_ltv','original_int_rt','channel','ppm_flag','product_type','property_state', 'prop_type','zipcode','loan_seq_number','loan_purpose', 'original_loan_term','number_of_borrowers','sellers_name','servicer_name','super_conforming_flag'],skipinitialspace=True)   
        df.to_csv(file, header=True,index=False, mode='a')
        print("%s csv generated!"%file )
        
    with open(f2, 'w',encoding='utf-8') as file: 
        df = pd.read_csv(testfile ,delimiter ="|", names=['credit_score','first_payment_date','fthb_flag','matr_date','msa',"mortage_insurance_pct",'no_of_units','occupancy_status','cltv','dti_ratio','original_upb','original_ltv','original_int_rt','channel','ppm_flag','product_type','property_state', 'prop_type','zipcode','loan_seq_number','loan_purpose', 'original_loan_term','number_of_borrowers','sellers_name','servicer_name','super_conforming_flag'],skipinitialspace=True)   
        df.to_csv(file, header=True,index=False, mode='a')
        print("%s csv generated!"%file )


# In[22]:


login ('a','b','c','d')


# In[1]:


def constructperformancecsv(filename):##Changed
    print("Started",filename)
    writeHeader1 = True
    #filename = "HistoricalperformanceCombined.csv"
    download_path = r'C:\Users\Komal\Desktop\Untitled Folder\\'
    final_sample = pd.DataFrame()
    for subdir,dirs, files in os.walk(download_path):
        for file in files:
            #print(file," ",filename)
            if filename == file: ##Changed
                temp_list = []
                chunksize = 10 ** 5
                for chunk in pd.read_csv(os.path.join(subdir,file) ,sep="|",                                          skipinitialspace=True, chunksize=chunksize, low_memory=False, header=None):
                    temp_list.append(chunk)
                print('DataFrame creation started!!')
                frames = []
                for df in temp_list:
                    frames.append(df)
                sample_df = pd.concat(frames)
                
                
                final_sample=pd.concat([final_sample, sample_df])
                
    return final_sample


# In[2]:


trainQ = 'Q12005'
file_name = r"historical_data1_time_"+ trainQ + ".txt"


# In[5]:


Performance_data= constructperformancecsv(file_name)


# In[9]:


Performance_data.info()


# In[11]:


Performance_data.head()


# In[13]:


Performance_data.columns = ['id_loan','mon_rpt_prd','current_aupb','curr_ln_delin_status','loan_age','remng_mon_to_leg_matur', 'repurch_flag','mod_flag','zero_bal_cd', 'zero_bal_eff_dt','current_int_rte','current_dupb','lst_pd_inst_duedt','mi_recoveries', 'net_sale_proceeds','non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs','taxes_and_insur','misc_expenses','actual_loss_calc', 'mod_cost','stepmod_ind', 'dpm_ind' , 'eltv']


# In[14]:


Performance_data.head()


# In[15]:


def performance_fillNA(perf_df):
    perf_df['curr_ln_delin_status'] = perf_df['curr_ln_delin_status'].fillna(0)
    perf_df['repurch_flag']=perf_df['repurch_flag'].fillna('Unknown')
    perf_df['mod_flag']=perf_df['mod_flag'].fillna('N')
    perf_df['zero_bal_cd']=perf_df['zero_bal_cd'].fillna(00)
    perf_df['zero_bal_eff_dt']=perf_df['zero_bal_eff_dt'].fillna('199601')
    perf_df['current_dupb']=perf_df['current_dupb'].fillna(0)
    perf_df['lst_pd_inst_duedt']=perf_df['lst_pd_inst_duedt'].fillna('199601')
    perf_df['mi_recoveries']=perf_df['mi_recoveries'].fillna(0)
    perf_df['net_sale_proceeds']=perf_df['net_sale_proceeds'].fillna('U')
    perf_df['non_mi_recoveries']=perf_df['non_mi_recoveries'].fillna(0)
    perf_df['expenses']=perf_df['expenses'].fillna(0)
    perf_df['legal_costs']=perf_df['legal_costs'].fillna(0)
    perf_df['maint_pres_costs']=perf_df['maint_pres_costs'].fillna(0)
    perf_df['taxes_and_insur']=perf_df['taxes_and_insur'].fillna(0)
    perf_df['misc_expenses']=perf_df['misc_expenses'].fillna(0)
    perf_df['actual_loss_calc']=perf_df['actual_loss_calc'].fillna(0)
    perf_df['mod_cost']=perf_df['mod_cost'].fillna(0)
    
    return perf_df


# In[16]:


clean_df = performance_fillNA(Performance_data)


# In[17]:


def statusUpdate(df):
    df['delinquent'] = (df.curr_ln_delin_status > 0).astype(int)
    return df


# In[20]:


clean_df.info()


# In[21]:


def changeperformancedatatype(perf_df):
        perf_df[['curr_ln_delin_status','loan_age','remng_mon_to_leg_matur','zero_bal_cd','current_dupb',                 'actual_loss_calc']] = perf_df[['curr_ln_delin_status','loan_age','remng_mon_to_leg_matur',                                                 'zero_bal_cd','current_dupb','actual_loss_calc']].astype('int64')

        perf_df[['mon_rpt_prd','zero_bal_eff_dt','lst_pd_inst_duedt']] = perf_df[['mon_rpt_prd','zero_bal_eff_dt',                                                                                  'lst_pd_inst_duedt']].astype('str')
        return perf_df


# In[ ]:


cleandf.


# In[22]:


data = changeperformancedatatype(clean_df)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




