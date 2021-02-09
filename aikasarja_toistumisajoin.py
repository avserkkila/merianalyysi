#!/usr/bin/python3

import numpy as n
from matplotlib.pyplot import *
from matplotlib.colors import ListedColormap

jaaraja = "15_1";
uk = '/home/aerkkila/a/kuvat1/';

#varit = ('r', 'g', 'b', 'm', 'c', 'k');

nimet = ["A: 4.5", "A: 8.5", "B: 4.5", "B: 8.5", "D: 4.5", "D: 8.5"];
ajot = ["A002", "A005", "B002", "B005", "D002", "D005"];

#pienin ja suurin mukaanotettava toistumisaika
T0 = 2;
T1 = 100;

#kaavat värien laskemiselle värikartassa
#vihr1 = lambda c: n.tanh(n.abs((0 if(c < 1/2) else 1) - c) * 5);
vihr = lambda c: n.abs(n.sin(c*n.pi*20)**0.6)

pun = lambda c: c**0.5;
sin = lambda c: 1 - pun(c);

Tarr = n.array(range(T0, T1+1));
Tarr = Tarr[::-1]; #suunnanvaihdos koska kuva toimii näin päin

#pinta-alan yhtälö toistumisajan funktiona sovitussuoran parametreista
pa_l = lambda T,a,b: (-n.log(-n.log(1/T))-b) / a;

figure(figsize=(12,10));
for aind in range(len(ajot)):
    
    #luetaan suoran parametrit
    tied = "gumbkertoimet_%s_%s.txt" %(jaaraja,ajot[aind]);
    data = n.genfromtxt(tied, usecols=[0,1,3]); #a, b, vuosi
    a = data[:,0];
    b = data[:,1];
    v = data[:,2];
    rajat = [min(v), max(v), T0, T1];

    #pinta-alat kaikista toistumisajoista
    #a ja b ovat taulukoita, joten tässä on kaikki vuodet
    A = [[]]*(T1+1-T0);
    tmp = 0;
    for T in Tarr:
        A[tmp] = pa_l(T,a,b);
        tmp+=1;
    A = n.array(A);

    #tehdään rgb-värikartta halutusta pinta-alavälistä
    A0 = 0; A1 = 100000;
    varit = [[]]*256
    c = n.linspace(0,1,256);
    for tmp in range(256):
        varit[tmp] = [pun(c[tmp]), vihr(c[tmp]), sin(c[tmp]), 1];
    vkartta = ListedColormap(varit);

    subplot(3,2,aind+1);
    kuva = imshow(A, cmap=vkartta, extent=rajat, aspect='auto');
    xlabel("vuosiluku");
    ylabel("toistumisaika (vuotta)");
    title('%s' %(nimet[aind]));
    colorbar(label="pinta-ala ($km^2$)");
tight_layout(h_pad=1);
if 1:
    show();
else:
    savefig(uk + "pa_x_"+jaaraja+".png");
