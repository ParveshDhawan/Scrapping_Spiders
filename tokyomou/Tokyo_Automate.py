# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 11:33:24 2019

@author: ParveshDhawan
"""
from bs4 import BeautifulSoup
import pandas as pd
import requests
import operator
from datetime import date,timedelta

from selenium import webdriver
driver = webdriver.Chrome(r'D:/Scrapper_Scripts/chromedriver.exe')
driver.get('https://apcis.tmou.org/public/')
cookies = driver.get_cookies()
# driver.quit()

from_date = date.today() - timedelta(days=365) 
to_date = date.today()
print(to_date)
print(from_date)
final_df = pd.DataFrame(columns=['Date','Authority','Port','Incp_Type','Detention','ShipName','ShipIMO','MMSI','Callsign','Class_Society','Flag','Vesseltyp','DateKeelLaid','DWT','Tonnage','Company_Name','Company_IMO','Residence','Registered','Phone','Fax','Email','Deficiency','Ship_Deficiency'])

# #Main Data to be carried out
Date = []
Authority = []
Port = []
Incp_Type = []
Detention = []

#Ship data
ShipName = []
ShipIMO = []
MMSI = []
Callsign = []
Class_Society = []
Flag = []
Vesseltyp = []
DateKeelLaid = []
DWT = []
Tonnage = []

#Company Data
Company_Name = []
Company_IMO = []
Residence = []
Registered = []
Phone = []
Fax = []
Email = []

#Entire Deficiency in One
Deficiency = []
Ship_Deficiency = []


with requests.Session() as s:
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    s.headers.update(headers)
    for cookie in cookies:
        c = {cookie['name']: cookie['value']}
    s.cookies.update(c)
 #Get Captcha
    r_get = s.get('https://apcis.tmou.org/public/?action=login')
    soup = BeautifulSoup(r_get.text,'lxml')
    content = soup.find_all('span')[0].text
    
 #Captcha solved
    ops = { "+": operator.add, "-": operator.sub, "*":operator.mul, "/":operator.floordiv }
    val = ops[content[2]](int(content[0]),int(content[4]))
    
#Making Post
    payload = {'captcha':val}
    r_post = s.post('https://apcis.tmou.org/public/?action=login',data=payload)
    
 #Next Post
    var = {'imo':'',
           'callsign':'',
           'name':'',
           'compimo':'',
           'compname':'',
           'From':'2019-01-01',#str(str(from_date)[-2:]+'.'+str(from_date)[5:7]+'.'+str(from_date)[:4]),
           'Till':'2020-07-13',#str(str(to_date)[-2:]+'.'+str(to_date)[5:7]+'.'+str(to_date)[:4]),
           'authority':0,
           'flag':0
           ,'class':0,
           'ro':0,
           'type':0,
           'result':0,
           'insptype':-1,
           'sort1':0,
           'sort2':'DESC',
           'sort3':0,
           'sort4':'DESC'}
    data_table = s.post('https://apcis.tmou.org/public/?action=getinspections',data=var)  
    datasoup = BeautifulSoup(data_table.text,'lxml')
    
    #Carrying out Pages count
    pages = int(datasoup.find('ul').text.split()[4])
    
    #all IDS for further digg
    ids = []
    main_data = []
    for i in datasoup.find_all('tr'):
        for j in i.find_all('input'):
            ids.append(j['value'])
        
        # # For below count of Deficiencies
        for j in i.find_all('td'):
            main_data.append(j.text)
    
    main_data = main_data[4:]
    n = 11 #Chunking at 11
    main_data = [main_data[i * n:(i + 1) * n] for i in range((len(main_data) + n - 1) // n )]
    deficiencies = [int(main_data[i][8]) for i in range(len(main_data))]
    
 #Making Post
    for i in range(len(ids)):
        load = {'UID':ids[i]}
        df = s.post('https://apcis.tmou.org/public/?action=getshipinsp',data=load)
        df = BeautifulSoup(df.text,'lxml')
        
        #Inspection Data
        p = df.find('table')
        p_data = [i.text for i in p.find_all('td')]
        #print(p_data)
        
        Date.append(p_data[0])
        Authority.append(p_data[1])
        Port.append(p_data[2])
        Incp_Type.append(p_data[3])
        Detention.append(p_data[4])
        
        #Ship Data
        q = p.findNextSibling('table')
        q_data = [i.text for i in q.find_all('td')]
        #print(q_data)

        ShipName.append(q_data[0])
        ShipIMO.append(q_data[1])
        MMSI.append(q_data[2])
        Callsign.append(q_data[3])
        Class_Society.append(q_data[4])
        Flag.append(q_data[5])
        Vesseltyp.append(q_data[6])
        DateKeelLaid.append(q_data[7])
        DWT.append(q_data[8])
        Tonnage.append(q_data[9])
        
        
        try:
            #Company Data
            R = q.findNextSibling('table')
            R_data = [i.text for i in R.find_all('td')]
            #print(R_data)
    
            Company_Name.append(R_data[0])
            Company_IMO.append(R_data[1])
            Residence.append(R_data[2])
            Registered.append(R_data[3])
            Phone.append(R_data[4])
            Fax.append(R_data[5])
            Email.append(R_data[6])
            
    
            if int(deficiencies[i]) == 0:
                Ship_Deficiency.append(0)
            else:
                #Ship Deficiencies
                S = R.find_next_sibling('table')
                T = S.find_next_sibling('table')
                T_data = [i.text for i in T.find_all('td')]
                Ship_Deficiency.append(T_data)
                
            Deficiency.append(deficiencies[i])
        except:
            Company_Name.append(0)
            Company_IMO.append(0)
            Residence.append(0)
            Registered.append(0)
            Phone.append(0)
            Fax.append(0)
            Email.append(0)
            Ship_Deficiency.append(0)
            Deficiency.append(deficiencies[i])
        
        
########################################################################
## For loopin to multiple pages

    for page in range(1,pages + 1):
        page_update = {'Page':page,
                       'imo':'',
                       'callsign':'',
                       'name':'',
                       'compimo':'',
                       'compname':'',
                       'From':'2019-01-01',#str(str(from_date)[-2:]+'.'+str(from_date)[5:7]+'.'+str(from_date)[:4]),
                       'Till':'2020-07-13',#str(str(to_date)[-2:]+'.'+str(to_date)[5:7]+'.'+str(to_date)[:4]),
                       'authority':0,
                       'flag':0,
                       'class':0,
                       'ro':0,
                       'type':0,
                       'result':0,
                       'insptype':-1,
                       'sort1':0,
                       'sort2':'DESC',
                       'sort3':0,
                       'sort4':'DESC'}
        
        print('-------------------------------------------------------------------------------------------------> ',page)
        #time.sleep(5)
        data_table = s.post('https://apcis.tmou.org/public/?action=getinspections',data=page_update)  
        datasoup = BeautifulSoup(data_table.text, 'lxml')
        
        #all IDS for further digg
        ids = []
        main_data = []
        for i in datasoup.find_all('tr'):
            for j in i.find_all('input'):
                ids.append(j['value'])

            # # For below count of Deficiencies
            for j in i.find_all('td'):
                main_data.append(j.text)

        main_data = main_data[4:]
        n = 11 #Chunking at 11
        main_data = [main_data[i * n:(i + 1) * n] for i in range((len(main_data) + n - 1) // n )]
        deficiencies = [int(main_data[i][8]) for i in range(len(main_data))]

     #Making Post
        for i in range(len(ids)):
            load = {'UID':ids[i]}
            df = s.post('https://apcis.tmou.org/public/?action=getshipinsp',data=load)
            df = BeautifulSoup(df.text, 'lxml')

            #Inspection Data
            p = df.find('table')
            p_data = [i.text for i in p.find_all('td')]
            #print(p_data)

            Date.append(p_data[0])
            Authority.append(p_data[1])
            Port.append(p_data[2])
            Incp_Type.append(p_data[3])
            Detention.append(p_data[4])

            #Ship Data
            q = p.findNextSibling('table')
            q_data = [i.text for i in q.find_all('td')]
            #print(q_data)

            ShipName.append(q_data[0])
            ShipIMO.append(q_data[1])
            MMSI.append(q_data[2])
            Callsign.append(q_data[3])
            Class_Society.append(q_data[4])
            Flag.append(q_data[5])
            Vesseltyp.append(q_data[6])
            DateKeelLaid.append(q_data[7])
            DWT.append(q_data[8])
            Tonnage.append(q_data[9])

            try:
                #Company Data
                R = q.findNextSibling('table')
                R_data = [i.text for i in R.find_all('td')]
                #print(R_data)
    
                Company_Name.append(R_data[0])
                Company_IMO.append(R_data[1])
                Residence.append(R_data[2])
                Registered.append(R_data[3])
                Phone.append(R_data[4])
                Fax.append(R_data[5])
                Email.append(R_data[6])
    
    
                if int(deficiencies[i]) == 0:
                    Ship_Deficiency.append(0)
                else:
                    #Ship Deficiencies
                    S = R.find_next_sibling('table')
                    T = S.find_next_sibling('table')
                    T_data = [i.text for i in T.find_all('td')]
                    # n=4
                    # T_data = [T_data[i * n:(i + 1) * n] for i in range((len(T_data) + n - 1) // n )]
                    #print(T_data)
                    Ship_Deficiency.append(T_data)
    
                Deficiency.append(deficiencies[i])
            except:
                Company_Name.append(0)
                Company_IMO.append(0)
                Residence.append(0)
                Registered.append(0)
                Phone.append(0)
                Fax.append(0)
                Email.append(0)
                Ship_Deficiency.append(0)
                Deficiency.append(deficiencies[i])

final_df = pd.DataFrame(list(zip(Date,Authority,Port,Incp_Type,Detention,ShipName,ShipIMO,MMSI,Callsign,
                                 Class_Society,Flag,Vesseltyp,DateKeelLaid,DWT,Tonnage,Company_Name,Company_IMO,
                                 Residence,Registered,Phone,Fax,Email,Deficiency,Ship_Deficiency)),
                        columns=['Date','Authority','Port','Incp_Type','Detention','ShipName','ShipIMO',\
                                'MMSI','Callsign','Class_Society','Flag','Vesseltyp','DateKeelLaid','DWT',\
                                'Tonnage','Company_Name','Company_IMO','Residence','Registered','Phone',\
                                'Fax','Email','Deficiency','Ship_Deficiency'])

final_df.to_csv('D://Tokyo_Current_Scrapped.csv',index=False)

driver.quit()
# df = pd.read_csv('D:/Daily_Data/Tokyo_Daily_Scrapped_data.csv')

# df = pd.concat([df,final_df])

# df['Ship_Deficiency'] = df['Ship_Deficiency'].astype('str')

# df = df.drop_duplicates()
# print(df.shape)

# df.to_csv('D:/Daily_Data/Tokyo_Daily_Scrapped_data.csv',index = False)
# df.to_csv('D:/Scrapper_Scripts/Tokyo_Daily_Scrapped_data.csv',index = False)
