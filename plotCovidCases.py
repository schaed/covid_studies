#!/usr/bin/env python
"""
Plot the new daily COVID-19 cases in different countries
"""
__author__ = "Stanislava Sevova"
###############################################################################
# Import libraries
################## 
import argparse
import sys
import os
import re
import glob
import shutil
#import uproot as up
#import uproot_methods
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import glob
from plotUtils import *
###############################################################################
# Command line arguments
######################## 
def getArgumentParser():
    """ Get arguments from command line"""
    parser = argparse.ArgumentParser(description="Plotting the daily covid numbers in various countries")
    parser.add_argument('-i',
                        '--infile',
                        dest='infile',
                        help='Input CSV file',
                        default='/afs/cern.ch/work/s/ssevova/public/covid_studies/owid-covid-data.csv')
    parser.add_argument('-o',
                        '--outdir',
                        dest='outdir',
                        help='Output directory for plots, selection lists, etc',
                        default='outdir')
    
    return parser
###############################################################################
def main():
    """ Run script """

    options = getArgumentParser().parse_args()
    
    ### Make output dir
    dir_path = os.getcwd()
    out_dir = options.outdir
    path = os.path.join(dir_path, out_dir)
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    os.chdir(path)

    df_all = pd.read_csv(options.infile)

    #df_swiss_official = pd.read_csv(options.infile)
    df_swiss = df_all[df_all['location']=='Switzerland']
    df_bgr   = df_all[df_all['location']=='Bulgaria']
    df_usa   = df_all[df_all['location']=='United States']
    df_can   = df_all[df_all['location']=='Canada']
    df_pol   = df_all[df_all['location']=='Poland']
    df_france = df_all[df_all['location']=='France']
    df_spain = df_all[df_all['location']=='Spain']

    df_europe = df_all[df_all['continent']=='Europe']
    
    
    df_bgr = pd.merge(df_swiss, df_bgr, how='outer', on='date').fillna(0)
    df_pol = pd.merge(df_swiss, df_pol, how='outer', on='date').fillna(0)
    
    labelDay="Cases / day"
    labelMil="Cases per million / day"
    isLog=False

    #make1Dplot(df_swiss_official['new.infections'],"daily_infections",0,len(df_swiss_official.index),labelDay,isLog)
    make1Dplot(df_can['new_cases']  ,"canada_daily_infections",0,len(df_can.index),labelDay,isLog)
    make1Dplot(df_swiss['new_cases'],"swiss_daily_infections",0,len(df_swiss.index),labelDay,isLog)
    make1Dplot(df_bgr['new_cases_y']  ,"bgr_daily_infections",0,len(df_bgr.index),labelDay,isLog)
    make1Dplot(df_usa['new_cases']  ,"usa_daily_infections",0,len(df_usa.index),labelDay,isLog)
    make1Dplot(df_france['new_cases']  ,"france_daily_infections",0,len(df_france.index),labelDay,isLog)
    make1Dplot(df_spain['new_cases']  ,"spain_daily_infections",0,len(df_spain.index),labelDay,isLog)
    
    make1Dplot(df_can['new_cases_per_million'],"canada_daily_cases_per_mil",0,len(df_can.index),labelMil,isLog)
    make1Dplot(df_swiss['new_cases_per_million'],"swiss_daily_cases_per_mil",0,len(df_swiss.index),labelMil,isLog)
    make1Dplot(df_bgr['new_cases_per_million_y'],"bgr_daily_cases_per_mil",0,len(df_bgr.index),labelMil,isLog)
    make1Dplot(df_usa['new_cases_per_million'],"usa_daily_cases_per_mil",0,len(df_usa.index),labelMil,isLog)
    make1Dplot(df_france['new_cases_per_million'],"france_daily_cases_per_mil",0,len(df_france.index),labelMil,isLog)
    make1Dplot(df_spain['new_cases_per_million'],"spain_daily_cases_per_mil",0,len(df_spain.index),labelMil,isLog)

    df_can.loc[df_can['new_cases_per_million']<1,'new_cases_per_million']=0.0
    df_usa.loc[df_usa['new_cases_per_million']<1,'new_cases_per_million']=0.0
    df_swiss.loc[df_swiss['new_cases_per_million']<1,'new_cases_per_million']=0.0
    
    make1DplotCompare(df_can['new_cases_per_million'],"Canada",df_usa['new_cases_per_million'],"USA","can_v_usa_per_mil",labelMil,isLog)
    make1DplotCompare(df_swiss['new_cases_per_million'],"Switzerland",df_usa['new_cases_per_million'],"USA","swiss_v_usa_per_mil",labelMil,isLog)
    make1DplotCompare(df_swiss['new_cases_per_million'],"Switzerland",df_can['new_cases_per_million'],"Canada","swiss_v_can_per_mil",labelMil,isLog)
    make1DplotCompare(df_swiss['new_cases_per_million'],"Switzerland",df_bgr['new_cases_per_million_y'],"Bulgaria","swiss_v_bgr_per_mill",labelMil,isLog)
    make1DplotCompare(df_swiss['new_cases_per_million'],"Switzerland",df_pol['new_cases_per_million_y'],"Poland","swiss_v_pol_per_mill",labelMil,isLog)
    make1DplotCompare(df_can['new_cases_per_million'],"Canada",df_bgr['new_cases_per_million_y'],"Bulgaria","can_v_bgr_per_mill",labelMil,isLog)
    make1DplotCompare(df_usa['new_cases_per_million'],"USA",df_spain['new_cases_per_million'],"Spain","usa_v_spain_per_mill",labelMil,isLog)
    make1DplotCompare(df_usa['new_cases_per_million'],"USA",df_france['new_cases_per_million'],"France","usa_v_france_per_mill",labelMil,isLog)
    
    make1DplotCompare(df_usa['new_cases_per_million'],"USA cases",df_usa['new_deaths_per_million'],"USA deaths","usa_cases_v_deaths_per_mill",labelMil,True)
    make1DplotCompare(df_can['new_cases_per_million'],"CAN cases",df_can['new_deaths_per_million'],"CAN deaths","can_cases_v_deaths_per_mill",labelMil,True)
    make1DplotCompare(df_swiss['new_cases_per_million'],"SWISS cases",df_swiss['new_deaths_per_million'],"SWISS deaths","swiss_cases_v_deaths_per_mill",labelMil,True)
    make1DplotCompare(df_france['new_cases_per_million'],"FRANCE cases",df_france['new_deaths_per_million'],"FRANCE deaths","france_cases_v_deaths_per_mill",labelMil,True)
    make1DplotCompare(df_spain['new_cases_per_million'],"SPAIN cases",df_spain['new_deaths_per_million'],"SPAIN deaths","spain_cases_v_deaths_per_mill",labelMil,True)
    
    makeHTML("covid19_cases.html","COVID-19 plots")
    
if __name__ == '__main__':
    main()
