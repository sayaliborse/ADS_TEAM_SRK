#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
import shutil
import urllib
import zipfile
import logging 
import requests
import webbrowser
import pandas as pd
import urllib.request
import mechanicalsoup as ms
from io import BytesIO
from requests import get 
from pathlib import Path
from zipfile import ZipFile
from bs4 import BeautifulSoup
import webbrowser


# In[11]:


def login(login, password):
    url = "https://freddiemac.embs.com/FLoan/secure/auth.php"
    url2 = "https://freddiemac.embs.com/FLoan/Data/download.php"

    #webbrowser.open(url)
    s = requests.Session()
    print(s)

    browser = ms.Browser(session = s)
    print("Logging in ....")

    login_page = browser.get(url)
    login_form = login_page.soup.find("form", {"class":"form"})
    login_form.find("input" , {"name": "username"})["value"] = login
    login_form.find("input" , {"name": "password"})["value"] = password

    response = browser.submit(login_form , login_page.url)
    login_page2 = browser.get(url2)
    print("To the continue page....")
    
    next_form = login_page2.soup.find("form" , {"class" : "fmform"})
    a = next_form.find("input" , {"name" : "accept"}).attrs
    a ['checked'] =  True

    response2 = browser.submit(next_form , login_page2.url)
    print("Start Downloading from..." + response2.url)

    table = response2.soup.find("table" , {"class" : "table1"})
    t = table.find_all('a')

    for x in range(81,94):
        c = 'https://freddiemac.embs.com/FLoan/Data/' + t[x]['href']
        print(c)
        r = s.get(c)
        z = ZipFile(BytesIO(r.content)) 
        z.extractall(os.getcwd() + '/All_Samples')  
    
    
    print("Downloaded all sample successfully!")


# In[ ]:





# In[13]:


def orig_cleaning(orig_df):
    orig_df['cred_scr'] = orig_df['cred_scr'].fillna(0)
    orig_df['fst_hmebyr_flg']=orig_df['fst_hmebyr_flg'].fillna('Unknown')
    orig_df['metro_stat_area']=orig_df['metro_stat_area'].fillna(0)
    orig_df['mort_insur_pctg']=orig_df['mort_insur_pctg'].fillna(0)
    orig_df['nbr_units']=orig_df['nbr_units'].fillna(0)
    orig_df['occu_status']=orig_df['occu_status'].fillna('Unknown')
    orig_df['orig_cmbnd_ln_to_value']=orig_df['orig_cmbnd_ln_to_value'].fillna(0)
    orig_df['orig_dbt_to_incm']=orig_df['orig_dbt_to_incm'].fillna(0)
    orig_df['orig_ln_to_value']=orig_df['orig_ln_to_value'].fillna(0)
    orig_df['chnl']=orig_df['chnl'].fillna('Unknown')
    orig_df['pre_pnl_mort_flg']=orig_df['pre_pnl_mort_flg'].fillna('Unknown')
    orig_df['proptype']=orig_df['proptype'].fillna('Unknown')
    orig_df['zipcode']=orig_df['zipcode'].fillna(0)
    orig_df['ln_purps']=orig_df['ln_purps'].fillna('Unknown')
    orig_df['nbr_brwrs']=orig_df['nbr_brwrs'].fillna(0)
    orig_df['spr_confrm_flg']=orig_df['spr_confrm_flg'].fillna('N')
    
    return orig_df


# In[ ]:





# In[4]:


def combineOrigFiles():
    print('Starting creation of combined Origination File!!', '\n')
    filedirectory_path = './All_Samples/'
    combinedfile_name = filedirectory_path + 'OriginationCombined.csv'
    if os.path.exists(combinedfile_name):
        os.unlink(combinedfile_name)
    firstRun = 1
    
    for path, subdirs, files in os.walk(filedirectory_path):
        for file in files:
            if '_orig_' in file:
                actual_file = os.path.join(path, file)
                
                with open(actual_file, 'r', encoding='utf-8') as f:
                    orig_df = pd.read_csv(f, sep='|', names=['cred_scr', 'fst_paymnt_dte', 'fst_hmebyr_flg', 'maturty_dte',                                                              'metro_stat_area', 'mort_insur_pctg', 'nbr_units', 'occu_status',                                                             'orig_cmbnd_ln_to_value', 'orig_dbt_to_incm', 'orig_upb',                                                              'orig_ln_to_value', 'orig_intrst_rate', 'chnl', 'pre_pnl_mort_flg',                                                             'prodtype', 'propstate', 'proptype', 'zipcode', 'ln_sq_nbr',                                                              'ln_purps', 'orig_ln_trm', 'nbr_brwrs', 'slr_name', 'srvcr_name',                                                             'spr_confrm_flg'],                                           skipinitialspace=True, low_memory=False)
                    orig_df = orig_cleaning(orig_df)
                    orig_df[['cred_scr','metro_stat_area','mort_insur_pctg','nbr_units','orig_cmbnd_ln_to_value',                             'orig_dbt_to_incm','orig_upb','orig_ln_to_value','zipcode','orig_ln_trm', 'nbr_units']] =                             orig_df[['cred_scr','metro_stat_area','mort_insur_pctg','nbr_units','orig_cmbnd_ln_to_value',                                'orig_dbt_to_incm','orig_upb','orig_ln_to_value','zipcode','orig_ln_trm',                                'nbr_units']].astype('int64')
                    orig_df[['spr_confrm_flg','srvcr_name']] = orig_df[['spr_confrm_flg','srvcr_name']].astype('str')
                    
                    orig_df['Year_Orig'] = ['20'+x for x in (orig_df['ln_sq_nbr'].apply(lambda x: x[2:4]))]
                    
                    if firstRun == 1:
                        orig_df.to_csv(combinedfile_name, mode='a', header=True,index=False)
                        firstRun = 0
                    else:
                        orig_df.to_csv(combinedfile_name, mode='a', header=False,index=False)
    print('Combined Origination file created successfully!!', '\n')


# In[5]:


combineOrigFiles()


# In[ ]:





# In[5]:


def performance_cleaning(perf_df):
    perf_df['curr_ln_delin_status'] = perf_df['curr_ln_delin_status'].fillna(0)
    perf_df['repurch_flag']=perf_df['repurch_flag'].fillna('Unknown')
    perf_df['mod_flag']=perf_df['mod_flag'].fillna('N')
    perf_df['zero_bal_cd']=perf_df['zero_bal_cd'].fillna(00)
    perf_df['zero_bal_eff_dt']=perf_df['zero_bal_eff_dt'].fillna('999901')
    perf_df['current_dupb']=perf_df['current_dupb'].fillna(0)
    perf_df['lst_pd_inst_duedt']=perf_df['lst_pd_inst_duedt'].fillna('999901')
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


# In[ ]:





# In[6]:


def minmax(perf_df):
    new1_df = perf_df.groupby(['ln_sq_nbr'])['current_aupb'].min().to_frame(name = 'min_current_aupb').reset_index()
    new2_df = perf_df.groupby(['ln_sq_nbr'])['current_aupb'].max().to_frame(name = 'max_current_aupb').reset_index()
    new3_df = perf_df.groupby(['ln_sq_nbr'])['curr_ln_delin_status'].min().to_frame(name = 'min_curr_ln_delin_status').reset_index()
    new4_df = perf_df.groupby(['ln_sq_nbr'])['curr_ln_delin_status'].max().to_frame(name = 'max_curr_ln_delin_status').reset_index()
    new5_df = perf_df.groupby(['ln_sq_nbr'])['zero_bal_cd'].min().to_frame(name = 'min_zero_bal_cd').reset_index()
    new6_df = perf_df.groupby(['ln_sq_nbr'])['zero_bal_cd'].max().to_frame(name = 'max_zero_bal_cd').reset_index()
    new7_df = perf_df.groupby(['ln_sq_nbr'])['mi_recoveries'].min().to_frame(name = 'min_mi_recoveries').reset_index()
    new8_df = perf_df.groupby(['ln_sq_nbr'])['mi_recoveries'].max().to_frame(name = 'max_mi_recoveries').reset_index()
    new11_df = perf_df.groupby(['ln_sq_nbr'])['non_mi_recoveries'].min().to_frame(name = 'min_non_mi_recoveries').reset_index()
    new12_df = perf_df.groupby(['ln_sq_nbr'])['non_mi_recoveries'].max().to_frame(name = 'max_non_mi_recoveries').reset_index()
    new13_df = perf_df.groupby(['ln_sq_nbr'])['expenses'].min().to_frame(name = 'min_expenses').reset_index()
    new14_df = perf_df.groupby(['ln_sq_nbr'])['expenses'].max().to_frame(name = 'max_expenses').reset_index()
    new15_df = perf_df.groupby(['ln_sq_nbr'])['legal_costs'].min().to_frame(name = 'min_legal_costs').reset_index()
    new16_df = perf_df.groupby(['ln_sq_nbr'])['legal_costs'].max().to_frame(name = 'max_legal_costs').reset_index()
    new17_df = perf_df.groupby(['ln_sq_nbr'])['maint_pres_costs'].min().to_frame(name = 'min_maint_pres_costs').reset_index()
    new18_df = perf_df.groupby(['ln_sq_nbr'])['maint_pres_costs'].max().to_frame(name = 'max_maint_pres_costs').reset_index()
    new19_df = perf_df.groupby(['ln_sq_nbr'])['taxes_and_insur'].min().to_frame(name = 'min_taxes_and_insur').reset_index()
    new20_df = perf_df.groupby(['ln_sq_nbr'])['taxes_and_insur'].max().to_frame(name = 'max_taxes_and_insur').reset_index()
    new21_df = perf_df.groupby(['ln_sq_nbr'])['misc_expenses'].min().to_frame(name = 'min_misc_expenses').reset_index()
    new22_df = perf_df.groupby(['ln_sq_nbr'])['misc_expenses'].max().to_frame(name = 'max_misc_expenses').reset_index()
    new23_df = perf_df.groupby(['ln_sq_nbr'])['actual_loss_calc'].min().to_frame(name = 'min_actual_loss_calc').reset_index()
    new24_df = perf_df.groupby(['ln_sq_nbr'])['actual_loss_calc'].max().to_frame(name = 'max_actual_loss_calc').reset_index()
    new25_df = perf_df.groupby(['ln_sq_nbr'])['mod_cost'].min().to_frame(name = 'min_mod_cost').reset_index()
    new26_df = perf_df.groupby(['ln_sq_nbr'])['mod_cost'].max().to_frame(name = 'max_mod_cost').reset_index()
    
    final_df = new1_df.merge(new2_df,on='ln_sq_nbr').merge(new3_df,on='ln_sq_nbr').merge(new4_df,on='ln_sq_nbr').    merge(new5_df,on='ln_sq_nbr').merge(new6_df,on='ln_sq_nbr').merge(new7_df,on='ln_sq_nbr').merge(new8_df,on='ln_sq_nbr').    merge(new11_df,on='ln_sq_nbr').merge(new12_df,on='ln_sq_nbr').merge(new13_df,on='ln_sq_nbr').merge(new14_df,on='ln_sq_nbr').    merge(new15_df,on='ln_sq_nbr').merge(new16_df,on='ln_sq_nbr').merge(new17_df,on='ln_sq_nbr').merge(new18_df,on='ln_sq_nbr').    merge(new19_df,on='ln_sq_nbr').merge(new20_df,on='ln_sq_nbr').merge(new21_df,on='ln_sq_nbr').merge(new22_df,on='ln_sq_nbr').    merge(new23_df,on='ln_sq_nbr').merge(new24_df,on='ln_sq_nbr').merge(new25_df,on='ln_sq_nbr').merge(new26_df,on='ln_sq_nbr')
    
    return final_df


# In[ ]:





# In[16]:


# Creating combined performance file
def combinePerfFiles():
    print('Starting creation of combined Performance File!!', '\n')
    filedirectory_path = './All_Samples/'
    combinedfile_name = filedirectory_path + 'PerformanceCombined.csv'
    if os.path.exists(combinedfile_name):
        os.unlink(combinedfile_name)
    firstRun = 1
    
    for path, subdirs, files in os.walk(filedirectory_path):
        for file in files:
            if '_svcg_' in file:
                actual_file = os.path.join(path, file)
                
                with open(actual_file, 'r', encoding='utf-8') as f:
                    perf_df = pd.read_csv(f ,sep="|", names=['ln_sq_nbr','mon_rpt_prd','current_aupb','curr_ln_delin_status',                                                             'loan_age','remng_mon_to_leg_matur', 'repurch_flag','mod_flag',                                                              'zero_bal_cd', 'zero_bal_eff_dt','current_int_rte','current_dupb',                                                             'lst_pd_inst_duedt','mi_recoveries', 'net_sale_proceeds',                                                             'non_mi_recoveries','expenses', 'legal_costs', 'maint_pres_costs',                                                             'taxes_and_insur','misc_expenses','actual_loss_calc', 'mod_cost',                                                             'step-mod', 'deferd_pymnt_modi','eltv'],                                          skipinitialspace=True, low_memory=False)
                    
                    perf_df['curr_ln_delin_status'] = [ 999 if x=='R' else x for x in                                                        (perf_df['curr_ln_delin_status'].apply(lambda x: x))]
                    perf_df['curr_ln_delin_status'] = [ 0 if x=='XX' else x for x in                                                        (perf_df['curr_ln_delin_status'].apply(lambda x: x))]
                    perf_df = performance_cleaning(perf_df)
                    
                    perf_df[['curr_ln_delin_status','loan_age','remng_mon_to_leg_matur','zero_bal_cd','current_dupb',                             'actual_loss_calc']] = perf_df[['curr_ln_delin_status','loan_age','remng_mon_to_leg_matur',                                                             'zero_bal_cd','current_dupb','actual_loss_calc']].astype('int64')

                    perf_df[['mon_rpt_prd','zero_bal_eff_dt','lst_pd_inst_duedt']] = perf_df[['mon_rpt_prd','zero_bal_eff_dt',                                                                                              'lst_pd_inst_duedt']].astype('str')
                    
                    filtered_df = minmax(perf_df)
                    
                    filtered_df['Year_Perf'] = ['20'+x for x in (filtered_df['ln_sq_nbr'].apply(lambda x: x[2:4]))]
                    
                    if firstRun == 1:
                        filtered_df.to_csv(combinedfile_name, mode='a', header=True,index=False)
                        firstRun = 0
                    else:
                        filtered_df.to_csv(combinedfile_name, mode='a', header=False,index=False)
    print('Combined Performance file created successfully!!', '\n')


# In[38]:


combinePerfFiles()


# In[ ]:



def main():
    user_input = sys.argv[1:]
    print("----Process Started----")
    username = sys.argv[1]   
    password = sys.argv[2]   
    login(username,password)
    combineOrigFiles()
    combinePerfFiles()
        
        
if __name__ == '__main__':
    main()


# In[ ]:




