# coding: utf-8
import os
import numpy as np
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from obspy import UTCDateTime
from multiprocessing import cpu_count
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from modules.askIRIS import askIRIS
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# *** Client tips: IRIS for CSN stations; GEONET for NZ stations;

client = 'GEONET'

# -- Kaimanawa
stations = {'NZ':['MCHZ', 'NMHZ', 'NTVZ', 'SNVZ', 'TMVZ','BKZ', 'ETVZ',
                  'KRHZ', 'KWHZ', 'MOVZ', 'MRHZ', 'OTVZ']}
components = ['HH*', 'EH*']
locations = ['10']

datadir = '/nobackup1c/faden/lfe_hikurangi/data'
#datadir = '/home/florent/work/lfe_hikurangi/data'

ncpu = 16 # number of cpu to use

for year in range(2008, 2021):
    print('Downloading year {}..'.format(year))
    start = UTCDateTime(year, 1, 1) # obspy.UTCDateTime only
    end = UTCDateTime(year, 1, 3) # obspy.UTCDateTime only

    askIRIS(datadir, client, stations, components, locations, start, end, ncpu)
