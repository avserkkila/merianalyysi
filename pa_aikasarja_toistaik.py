#!/usr/bin/python3

#piirtää n vuoden toistumisaikaa vastaavan pinta-alan vuosiluvun funktiona
#käytetään liukuvaa aikasarjaa

import numpy as np
import scipy.stats as st
from matplotlib.pyplot import *
import sys, locale
from jaettu import *

aikaikk = 45
tallenna = 0
try:
    aikaikk  = int(sys.argv[1])
    tallenna = int(sys.argv[2])
except:
    pass

Tn = [2, 5, 10, 30, 50] #halutut toistumisajat
#pinta-alan yhtälö toistumisajan funktiona sovitussuoran parametreista
pa_l = lambda T,a,b: (-np.log(-np.log(1/T))-b) / a

if suomeksi:
    xnimi = 'vuosi'
    ynimi = 'pinta-ala $(km^2)$'
    ulaotsikko = 'aikaikkuna = %i vuotta' %aikaikk
else:
    xnimi = 'year'
    ynimi = 'area $(km^2)$'
    ulaotsikko = 'time window = %i years' %aikaikk

figure(figsize=(12,10))
ytikit = np.linspace(0,80000,9)
ynimet = ["%.i" %luku if not i%2 else '' for i,luku in enumerate(ytikit)]
for aind in range(len(ajot)):
    tiedos = np.loadtxt('%s/makspintaalat_%s.txt'\
                      %(kansio, ajot[aind]), usecols=[0,2])
    if(aikaikk < 0):
        aikaikk = len(tiedos)
    v0 = tiedos[0,1]
    param = np.zeros((len(tiedos)-aikaikk+1,4))
    
    #muodostetaan juokseva aikasarja, jossa on kerrallaan mukana n vuotta
    #kun v on aikaikkunan 1. vuosi, keskiarvon vuodeksi laitetaan v+n/2
    #kun n on parillinen, takaa jää yksi vuosi vähemmän pois kuin edestä
    ind = 0
    while 1:
        pa = np.sort(tiedos[ind : ind+aikaikk, 0]) #valitaan aikaikkuna
        F = np.array(range(1,len(pa)+1)) / (len(pa)+1.0) #kokeellinen kertymäfunktio

        #rajataan ei-huomioitaviksi suoran sovituksessa kokonaisjäätymiset
        raja = len(pa)
        for tmp in range(len(pa)-1):
            if(pa[tmp] > 103000):
                raja = tmp
                break

        F = -1*np.log(-1*np.log(F)) #muunnos gumbelkoordinaatistoon

        #suoran sovitus sekä suoran parametrien ja vuoden tallentaminen
        a, b, r, p, kkv = st.linregress(pa[0:raja], F[0:raja])
        vuosi = v0+ind+(aikaikk-1)//2
        param[ind,:] = [a,b,r**2,vuosi]

        ind += 1
        if (ind+aikaikk > len(tiedos)):
            break
    
    #pinta-alat kaikista toistumisajoista
    #a ja b ovat taulukoita, joten tässä ovat kaikki vuodet
    A = [[]]*len(Tn)
    tmp = 0
    for T in Tn:
        A[tmp] = pa_l(T,param[:,0],param[:,1])
        tmp+=1
    A = np.array(A)
    A = A.transpose()

    subplot(3,2,aind+1)
    ylim(0,90000)
    plot(param[:,3], A, color='k')
    grid('on')
    yticks(ticks=ytikit, labels=ynimet, fontsize=13)
    viivat=gca().yaxis.get_gridlines()
    for i,viiva in enumerate(viivat):
        if not i%2:
            viiva.set_color('k')
        else:
            viiva.set_linestyle(':')
    xlabel(xnimi, fontsize=15)
    ylabel(ynimi, fontsize=15)
    xticks(fontsize=13)
    title('%s' %(ajonimet[aind]))

#r^2 oikealle y-akselille
    if 0:
        ax2 = gca().twinx()
        vari = 'lightskyblue'
        ax2.plot(param[:,3], param[:,2], color=vari)
        ylabel('$r^2$', rotation=0, fontsize=15, color=vari)
        yticks(fontsize=13, color=vari)
        locale.setlocale(locale.LC_ALL, paikallisuus)
        paikallista_akselit(0,1)
        ylim([0.85, 1])

suptitle(ulaotsikko)
tight_layout(h_pad=1)
if tallenna:
    savefig("%s/pa_aikasarja_toistaik_%i.png" %(kuvat, aikaikk))
else:
    show()