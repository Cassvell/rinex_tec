import pandas as pd
import tempfile, shutil, os
import numpy as np
import math

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl

from PIL import Image
from datetime import datetime, timedelta
import glob, os
import fnmatch 

import astropy.time as atime
from scipy.interpolate import interp1d
from scipy.stats import zscore


folder=input("write the folder name in format \n (code): ")
path_obs        = '/home/c-isaac/Documentos/rinex_ucoe/'+folder+'_cmn'+'/obs'
path_med        = '/home/c-isaac/Documentos/rinex_ucoe/'+folder+'_cmn'+'/med'

#file_names  = glob.glob(path+'/*.Cmn')


file_obs  = glob.glob(path_obs+'/*.Cmn')
file_med  = glob.glob(path_med+'/*.Cmn')

def df_tec_obs(files):
    dfs         = []
    mjdate      = []

    for file_name in files:
        df = pd.read_csv(file_name, header=2, sep='\s+', skip_blank_lines=True)
        #print(df)    
        date = df.pivot('Time', 'PRN', 'MJdatet')
        vtec = df.pivot('Time', 'PRN', 'Vtec')
        vtec_med = vtec.median(axis=1)        
        dfs.append(vtec_med)        
        date_med = date.median(axis=1)
        date_med = date_med.reset_index()
        mjdate.append(date_med)
         
    df_c    = pd.concat(dfs, axis=0, ignore_index=True)
    jdate   = pd.concat(mjdate, axis=0, ignore_index=True) 

    return(df_c, jdate)
################################################################################    
################################################################################
################################################################################

def df_tec_med(files):

    tec_med     = []

    for file_name in files:
        df = pd.read_csv(file_name, header=2, sep='\s+', skip_blank_lines=True)
        vtec = df.pivot('Time', 'PRN', 'Vtec')   
        vtec_med = vtec.median(axis=1)        
        
        tec_med.append(vtec_med)
    tecmed  = pd.concat(tec_med, axis=1, ignore_index=True)

    return(tecmed)

################################################################################    
################################################################################
################################################################################
def get_tec_median(data):
    data     = data.median(axis=1)

    data     = data.reset_index()

    med_sc  = zscore(data)
    ix      = np.abs(med_sc)
    fmed    = (ix < 1.6).all(axis=1)
    tmed    = data[fmed]

    tmed    = tmed.set_index(tmed['Time'])
    red_by  = 1
    tecm    = tmed.groupby(tmed.index//red_by).mean()
    print(len(tecm))
    del tecm['Time']
################################################################################
    pattern = '*.Cmn'
    filenames = next(os.walk(path_obs))[2]
    date_list = fnmatch.filter(filenames, pattern)
#date_list = date_list.sort()
    
    N       = len(date_list)
    Vmed_tec    = pd.concat([tecm]*N, ignore_index=True)


    #tecm = tmed.resample('1min').median()
    #Vmed_tec[0].plot()
    #plt.show()    
    return(Vmed_tec)

################################################################################    
################################################################################
################################################################################




def get_tec_obs(data1, data2):
    data1  = data1.iloc[:,1]
    t  = atime.Time(data1, format='mjd', scale='tt').iso
    #series = pd.date_range(start=t[0], end=t[-1], freq='H')
    #tec = df_c.set_index(['date'])

    time = []
    for i in t:
        #print(i)
        strdate = str(i)
        str2date= strdate[0:19]
        #print(str2date)
        date    = datetime.strptime(str2date, '%Y-%m-%d %H:%M:%S')
        time.append(date)

    tseries = pd.Series(time)

    tec_series = pd.concat([tseries, data2], axis=1, ignore_index=True)

    dtime = tec_series.iloc[:,0]
    vtec  = tec_series.iloc[:,1]

    tec_series = tec_series.set_index(dtime)


    #del tec_series.iloc[:,0]
    #print(tec_series)
    tec_obs = tec_series.resample('H').median()
    #tec_obs[1].plot()
      
    #plt.show()
    return(tec_obs)


#df_tec, df_date, df_tecmed = datframs_tec(file_names)

df_tec, df_date = df_tec_obs(file_obs)
df_tecmed       = df_tec_med(file_med)

tec_expected = get_tec_median(df_tecmed)
tec_observed = get_tec_obs(df_date, df_tec)
#tec_data     = pd.concat(tec_expected, tec_observed, axis=1, ignore_index=True)

medtec = tec_expected.iloc[:,0]


tec_observed = tec_observed.reset_index()
tec_observed['med'] = medtec.copy()

date_t       = tec_observed.iloc[:,0]
tec_obs      = tec_observed.iloc[:,1]
tec_med      = tec_observed.iloc[:,2]
#tec_observed = tec_observed.set_index(date_t)

#i_date = input("write initial date in format \n yyyy-mm-dd HH:MM:SS  " )
#f_date = input("write final date in format \n yyyy-mm-dd HH:MM:SS  " )

path_dst = '/home/c-isaac/Documentos/rinex_ucoe/dst/'
#file_name2 = path_dst+'Dst_'+i_date+'_'+f_date+'_Q.dat'
#df_dst = pd.read_csv(file_name2, header=22, sep='\s+', skip_blank_lines=True)


#dst = df_dst['Dst'] 


plt.plot(date_t, tec_obs, color='r', linewidth=1.0, label='TEC Obs')
plt.plot(date_t, tec_med, color='b', linewidth=1.0, label= 'TEC esp')
plt.grid()

plt.ylabel("TEC [TECu]")
plt.xlabel("Time [UTC]")

plt.legend()
lim_t = len(date_t)-1
plt.xlim([date_t[0], date_t[lim_t]])

plt.title("Respuesta ionosferica sobre Mexico en TEC")
#pathfig = '/home/c-isaac/Documentos/rinex_ucoe/vtec_figures'
plt.show()
plt.close()

'''

fig, (ax1, ax2)= plt.subplots(2)
fig.suptitle('Respuesta geomagnetica vs respuesta ionosferica')

fig.set_figheight(18)
fig.set_figwidth(15)

ax1.plot(date_t, tec_obs, color='r', linewidth=1.0, label='TEC Obs')
ax1.plot(date_t, tec_med, color='b', linewidth=1.0, label= 'TEC esp')
ax1.set_ylabel('TECu [nT]')
ax1.grid()
ax1.legend()
ax1.set_xlim([date_t[0], date_t[lim_t]])

ax2.plot(date_t, dst, 'k', linewidth=1.0)
ax2.set_ylabel('Dst [nT]')
ax2.grid()
ax2.set_xlim([date_t[0], date_t[lim_t]])
plt.show()

'''

