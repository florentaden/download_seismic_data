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

client = 'IRIS'

# stations is a dict whom keys are networks iD which contains list of stations
#stations = {'NZ':['MCHZ', 'NMHZ', 'NTVZ', 'SNVZ', 'TMVZ','BKZ', 'ETVZ',
#                  'KRHZ', 'KWHZ', 'MOVZ', 'MRHZ', 'OTVZ']}

#client = 'GFZ'
#stations = {'8F': ['AF01']}

#stations = {'C1':['MG01', 'MG02', 'MG03', 'MG04', 'MG05'], 'C': ['GO09', 'GO10'], 'AI': ['DSPA']}
#stations = {'XB': ['ALIE1', 'ALIE2', 'ALIE3', 'ALIE4', 'ALIE5']}
stations = {'XB': list(np.loadtxt('/home/florent/work/marlborough/catalogs/stations.latlon', usecols=(0), dtype=str))}

components = ['SH*'] # can be list of str or single str
locations = [''] # can be list of str or single str

#datadir = '/home/geovault-06/adenanto/hikurangi/data' # directory to save the data
#datadir = '/home/florent/work/atacama/data'
#datadir = '/home/florent/work/magallanes-fagnano/data'
datadir = '/home/florent/work/marlborough/data'
#datadir = '/home/florent/work/hikurangi/data'
ncpu = 1 # number of cpu to use

for year in [2001]:
    print('Downloading year {}..'.format(year))
    start = UTCDateTime(year, 1, 1) # obspy.UTCDateTime only
    end = UTCDateTime(year, 1, 10) # obspy.UTCDateTime only

    askIRIS(datadir, client, stations, components, locations, start, end, ncpu)
