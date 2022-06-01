import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import os
from os import listdir
from os.path import isfile, join
import re 
import datetime

def date_time(day,month,year):
    return datetime.datetime(int(year), int(month), int(day), 0, 0).strftime('%Y-%m-%d')    

#number of bikes at intersections
def read_data_velo_feu():

    df1=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2014_2016.csv")
    df2=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2017_2019.csv")
    df3=pd.read_csv("datasets/comptages_vehicules_cyclistes_pietons_2020_2022.csv")
    #view different automobiles that were tracked
    #set(df1['Description_Code_Banque'])
    return pd.concat([df1,df2,df3]).reset_index()

#number of bikes on cycling paths
def read_data_velo_piste():

    mypath='/home/apkhoury/Documents/projects/DataScience_Project/datasets'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    r = re.compile("comptage[v_].*")
    newlist = list(filter(r.match, onlyfiles))
    dfs=[]
    [dfs.append(pd.read_csv("datasets/"+x))for x in newlist]
    
    #adjusting month that is in french to regular dataset values
    dfs[8]['Date'][17376:20352]=dfs[8]['Date'][17376:20352].str.extract(r'([0-9]+)(\s\w+\.)(\s2021)(.*)')[[0,2,3]].apply(lambda row : date_time(row[0],7,row[2]), axis = 1)+dfs[8]['Date'][17376:20352].str.extract(r'([0-9]+)(\s\w+\.)(\s2021)(.*)')[3]+":00"
           
    # setting date and time in two different columns for datasets that have them in one column only
    for x in [0,4,6,8]:
        dfs[x]['Time'] = pd.to_datetime(dfs[x]['Date']).dt.time
        dfs[x]['Date'] = pd.to_datetime(dfs[x]['Date']).dt.date
    for y in [1,2,3,5,7]:
        dfs[y]['Date'] = pd.to_datetime(dfs[y]['Date']).dt.date

    #view different automobiles that were tracked
    #set(df1['Description_Code_Banque'])
    df=pd.concat(dfs)
    df.sort_values(by='Date',inplace=True)
    df.reset_index(inplace=True)
    return df

#coordinates of velo piste compteurs
def read_localisation_velos():
    df=pd.read_csv("datasets/localisation_des_compteurs_velo.csv")
    return df

#number of vehicules in montreal
def read_number_vehicles():
    df=pd.read_excel('datasets/tableau.xlsx',skiprows=5,skipfooter=17)
    df= df.set_index("Type d'utilisation").T
    return df

def read_air_quality_station():
    #only 2021 and 2022 data
    df=pd.read_csv("datasets/rsqa-indice-qualite-air-station-historique.csv")
    return df

def read_CO2():
    #2014 to 2018 data
    df=pd.read_csv('datasets/ghg-emissions-transport.csv')

if __name__ == "__main__":

    velo1=read_data_velo_feu()
    velo2=read_data_velo_piste()
    vehicule1=read_number_vehicules()

