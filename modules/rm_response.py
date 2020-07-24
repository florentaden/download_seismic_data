# coding: utf-8
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from obspy import read
from obspy.clients.fdsn import Client
from glob import glob
from itertools import product
from multiprocessing import Pool
from functools import partial
from sys import exit
from os import makedirs
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from modules_time import runtime
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

DEBUG = True

def rm_response_(trace_path, comps, locs, outdir, client):
    tr = read(trace_path)[0]
    network = tr.stats.network
    station = tr.stats.station
    channel = tr.stats.channel
    location = tr.stats.location
    start = tr.stats.starttime
    end = tr.stats.endtime

    try:
        tr.remove_response()
        print 'response was attached'
    except Exception, message:
        print message
        inv = None
        fdsn_client = Client(client)
        for comp, loc in product(comps[channel], locs[location]):
            try:
                inv = fdsn_client.get_stations(network=network, station=station,
                    location=loc, channel=comp, level='response',
                        starttime=start, endtime=end)
                break
            except Exception, message:
                print message
                pass

        if not inv:
            return 'reponse cound not be removed for trace: {}'.format(
                trace_path.split('/')[-1])

        inv[0][0][0].code = channel
        inv[0][0][0].location_code = location

        try:
            tr.remove_response(inv)
        except:
            return 'reponse cound not be removed for trace: {}'.format(
                trace_path.split('/')[-1])

    foldername = '{}/{}/{}'.format(outdir, station, start.year)
    try:
        makedirs(foldername)
    except Exception, message:
        pass

    print('writing')
    tr.write('{}/{}'.format(foldername, trace_path.split('/')[-1]),
        format='MSEED')



def rm_response(datadir, outdir, client, stas, comps, locs, start, end, ncpu):

    Nday = end.toordinal()-start.toordinal()
    if Nday == 1:
        dates = ['{}.{:03d}'.format(start.year, start.julday)]
    elif Nday > 1:
        dates = []
        for n in range(Nday):
            t = start + n*24*3600
            dates.append('{}.{:03d}'.format(t.year, t.julday))
    elif Nday <= 0:
        print "bad time period..."
        exit()

    traces_list = list()
    for sta, cha, date in product(stas, comps.keys(), dates):
        year = date.split('.')[0]
        traces_list += glob('{}/{}/{}/*{}.{}'.format(
            datadir, sta, year, cha, date))

    # --- remove response work
    runtime()
    if DEBUG:
        logs = map(partial(rm_response_, comps=comps, locs=locs,
            outdir=outdir, client=client), traces_list)
    else:
        pool = Pool(ncpu)
        logs = pool.map_async(partial(rm_response_, comps=comps, locs=locs,
            outdir=outdir, client=client), traces_list).get(9999999)
        pool.close()
        pool.join()
    runtime()
