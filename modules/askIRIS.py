# coding: utf-8
import numpy as np
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from obspy.clients.fdsn import Client
from obspy import read, UTCDateTime
from os.path import exists
from os import mkdir
from sys import exit
from multiprocessing import Pool
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

DEBUG = True

#def request2IRIS(args):
#    return _request2IRIS(*args)

def request2IRIS(fdsn_client, datadir, net, sta, comp, loc, time):
    starttime, endtime = time
    firstordinal = UTCDateTime(starttime.year, 1, 1).toordinal() - 1
    origin = '%d.%03d' %(starttime.year, starttime.toordinal()-firstordinal)

    try:
        st = fdsn_client.get_waveforms(network=net, station=sta,
                                       location=loc, channel=comp,
                                       starttime=starttime,
                                       endtime=endtime,
                                       attach_response=True)

        st.merge(fill_value=0)

        if not exists('{}/{}'.format(datadir, sta)):
            mkdir('{}/{}'.format(datadir, sta))
        if not exists('{}/{}/{}'.format(datadir, sta, starttime.year)):
            mkdir('{}/{}/{}'.format(datadir, sta, starttime.year))

        for tr in st:
            trace_name = '{}/{}/{}/{}.{}.{}.{}.{}'.format(datadir, sta,
                         starttime.year, net, sta, tr.stats.location,
                         tr.stats.channel, origin)
            tr.write(trace_name, format='MSEED')

    except Exception as message: # --- request failed
        print("download failed for: {} {} {} {} {} {}\n".format(net, sta,
               comp, loc, starttime, endtime))

def askIRIS(datadir, client, stas, comps, locs, starttime, endtime, ncpu):

    if not isinstance(comps, list):
        comps = [comps]
    if not isinstance(locs, list):
        locs = [locs]

    # --- initate client and request
    fdsn_client = Client(client)
    Nday = endtime.toordinal()-starttime.toordinal()

    if Nday == 1:
        starttimes = [starttime]
        endtimes = [endtime]
    elif Nday > 1:
        starttimes = [starttime + t for t in np.arange(Nday+1)*24*3600]
        endtimes = [starttime + t for t in np.arange(1, Nday+2)*24*3600]
    elif Nday <= 0:
        print("bad time period...")
        exit()


    # --- flattening of request to pool distribution
    times = list(zip(starttimes, endtimes))
    requests = [(fdsn_client, datadir,  k, sta, comp, loc, time) for k in stas.keys() \
                for sta in stas[k] for comp in comps for loc in locs for time in times]
    print('find {} requests..'.format(len(requests)))

    # --- loop
    pool = Pool(ncpu)
    logs = pool.starmap(request2IRIS, requests)
    pool.close()
    pool.join()
    print('request terminated')

    # TODO: write a better way to pass logs
    try:
        summary = '\n'.join(logs)
        return summary
    except:
        return 'ok'
