# coding: utf-8
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from modules.rm_response import rm_response
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from obspy import read, UTCDateTime
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

client = 'IRIS'
stations = ['MCHZ', 'NMHZ', 'NTVZ', 'SNVZ', 'TMVZ','BKZ', 'ETVZ',
                   'KRHZ', 'KWHZ', 'MOVZ', 'MRHZ', 'OTVZ']
components = {'Z': ['EHZ', 'HHZ'], 'E': ['EHE', 'HHE'], 'N': ['EHN', 'HHN']}
locations = {'': ['*']}

datadir = '/home/florent/work/hikurangi/processed_data'
outdir = '/home/florent/work/hikurangi/rmresponse_data'
ncpu = 20 # number of cpu to use

for year in [2015]:
    print('Processing year {}..'.format(year))
    start = UTCDateTime(year, 1, 1) # obspy.UTCDateTime only
    end = UTCDateTime(year, 1, 2) # obspy.UTCDateTime only

    print rm_response(datadir, outdir, client, stations, components, locations, start, end, ncpu)
