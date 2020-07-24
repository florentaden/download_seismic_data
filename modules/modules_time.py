""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from time import time
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def runtime(restart=False):
    global to
    if restart:
        to = time()
        return
    try:
        pasttime = (time()-to)/3600
        nhour = int(pasttime)
        nminu = int((pasttime-nhour)*60)
        nseco = int(((pasttime-nhour)*60-nminu)*60)
        print('{:02d}:{:02d}:{:02d} have passed..'.format(
            nhour, nminu, nseco))
    except:
        to = time()

if __name__ == '__main__':

    runtime()
    print to
    runtime()
