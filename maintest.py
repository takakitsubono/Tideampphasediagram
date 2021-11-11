# wrote 20211111
from ampang import AmpPhsDiagram
import numpy as np
import matplotlib.pyplot as plt

# test
cal=np.zeros((4))+[10.80-5.03j, 8.44-5.40j, 6.84-4.10j, 8.71-4.83j]
obs=np.zeros((4))+[14.78-0.45j,12.89-0.27j,11.21-0.14j,12.93-0.00j]
rat=cal/obs

smin=0.5
smax=1.5
swdt=0.25
tmin=-30.
tmax=30
twdt=15
aaa='ratio of magnitude(M2)(cal/obs)'
bbb='phase lag'
refft=1.0
    
arng=np.array((smin-0.10,smax+0.1))
prng=np.array((tmin-5.00,tmax+5.0))
athc=np.array((smin,smax,swdt))
pthc=np.array((tmin,tmax,twdt))

refstd=1.+0.0j
fig = plt.figure(figsize=(8,6))
dia = AmpPhsDiagram(reff=refft,fig=fig,amprange=arng,ampthck=athc,phsrange=prng,phsthck=pthc,amptitle=aaa,phstitle=bbb,rd_fmt="%.2f")
contours=dia.add_contours(levs=[0.2,0.4,0.6],colors='0.5')
plt.clabel(contours, inline=1, fontsize=10,fmt="%.1f")
plt.scatter(1,0,marker='*',s=70, label='refference')
plt.scatter(rat[0:4].real,rat[0:4].imag,marker='s', s=40, label='Cal/Obs')
plt.legend(loc="lower left",ncol=2,scatterpoints=1)
plt.savefig('ratio.png')

#ratio   test
smin=5.0
smax=15
swdt=2.5
tmin=-40.
tmax=20.
twdt=10.
aaa='ratio of magnitude(M2)(cal/obs)'
bbb='phase lag'
refft=np.abs(obs[3])
    
arng=np.array((smin-0.5,smax+0.5))
prng=np.array((tmin-2.0,tmax+2.0))
athc=np.array((smin,smax,swdt))
pthc=np.array((tmin,tmax,twdt))
    
fig = plt.figure(figsize=(8,6))
#dia = AmpPhsDiagram(reff=refft,fig=fig,amprange=arng,ampthck=athc,phsrange=prng,phsthck=pthc,amptitle=aaa,phstitle=bbb,rd_fmt="%.1f")
dia = AmpPhsDiagram(reff=refft,fig=fig,amprange=arng,ampthck=athc,phsrange=prng,phsthck=pthc,amptitle=aaa,phstitle=bbb)
contours=dia.add_contours(levs=[2.5,5.0,7.5],colors='0.5')
plt.clabel(contours, inline=1, fontsize=10,fmt="%.1f")
#plt.scatter(1,0,marker='*',s=70)
plt.scatter(obs[0:4].real,obs[0:4].imag,marker='s', s=40, color='orange',label='Obs.')
plt.scatter(obs[3].real,obs[3].imag,marker='s', s=42, color='orange',edgecolor='black')
plt.scatter(cal[0:4].real,cal[0:4].imag,marker='o', s=40, color='white',edgecolor='dodgerblue',label='Cal.')
plt.legend(loc="lower left",ncol=3,scatterpoints=1)
plt.savefig('orig.png')


#hilbert test
from scipy import signal
lp=2000
t0=np.arange(lp)
dt=np.arange(lp)/1000.
s0=t0*np.pi/100.
s1=t0*np.pi/(101.-dt)
s2=t0*np.pi/(99.+dt)
s3=t0*np.pi/99.
s4=t0*np.pi/101.

a =np.cos(s0)
b =(106-8*dt)/100*np.cos(s1)
c =( 94+8*dt)/100*np.cos(s2)
d =1.2*np.cos(s3)
e =0.8*np.cos(s4)

ah=signal.hilbert(a)
bh=signal.hilbert(b)
ch=signal.hilbert(c)
dh=signal.hilbert(d)
eh=signal.hilbert(e)

ttcs=np.cos(s0)+np.sin(s0)*1j
ahinv=ah/ttcs
bhinv=bh/ttcs
chinv=ch/ttcs
dhinv=dh/ttcs
ehinv=eh/ttcs

smin = 0.6
smax = 1.4
swdt = 0.2
tmin=-30.
tmax=30
twdt=15
aaa='score ratio'
bbb='phase lag'
arng=np.array((smin-0.1,smax+0.1))
prng=np.array((tmin-2.0,tmax+2.0))
athc=np.array((smin,smax,swdt))
pthc=np.array((tmin,tmax,twdt))
refft=1.0
fig = plt.figure(figsize=(8,6))
dia = AmpPhsDiagram(reff=refft,fig=fig,amprange=arng,ampthck=athc,phsrange=prng,phsthck=pthc,amptitle=aaa,phstitle=bbb,rd_fmt="%.1f")
contours=dia.add_contours(levs=[0.2,0.4,0.6],colors='0.5')
plt.clabel(contours, inline=1, fontsize=10,fmt="%.1f")
plt.scatter(ahinv[100].real,-ahinv[100].imag,label='A')
plt.plot(bhinv[500:1500].real,-bhinv[500:1500].imag,label='B')
plt.plot(chinv[500:1500].real,-chinv[500:1500].imag,label='C')
plt.plot(dhinv[500:1500].real,-dhinv[500:1500].imag,label='D')
plt.plot(ehinv[500:1500].real,-ehinv[500:1500].imag,label='E')
plt.legend(loc="lower left",ncol=3,scatterpoints=1)
plt.savefig('hilbert.png')

