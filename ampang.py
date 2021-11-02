#!/usr/bin/env python
# Copyright: This document has been placed in the public domain.
"""
Yannick Copin's pythoncode for Taylor diagram (Taylor, 2001) was changed to tidal amplitude & phase diagram by Takai Tsubono (2021/11/1)
Note: If you have found these software useful for your research, I would
appreciate an acknowledgment.
"""
__version__ = "modified from Time-stamp: <2018-12-06 11:43:41 ycopin>"
__author__ = " T. Tsubono modified from Yannick Copin's code "
import numpy as np
import matplotlib.pyplot as plt
class AmpPhsDiagram(object):
#" AmpPhs diagram.
#    Plot model constants of constituents and correlation to reference (data)
#    sample in a single-quadrant polar plot, r=amplitude and
#    theta= phaselag          .  "
    def __init__(self, reff=1.0, fig=None, rect=111, label='_', amprange=[0, 1.5],ampthck=[0,1.5,0.25],phsrange=[-30,30],phsthck=[-30,30,15],amptitle='amplitude',phstitle='phase lag'):
        """Set up amplitude and phase reffered to Taylor diagram axes, i.e. polar
        plot, using `mpl_toolkits.axisartist.floating_axes`.
        Parameters:
        * reff: reference standard deviation to be compared to
        * fig: input Figure or None
        * rect: subplot definition
        * label: reference label
        * amprange & phsrange: range angurar and radius
        * ampthck & phsthick : thick def. for angular and radius
        """
        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as FA
        import mpl_toolkits.axisartist.grid_finder as GF
        self.reff = reff            # Reference standard deviation
        self.amprange = amprange    
        self.phsrange = phsrange    
        idv = np.int( ( ampthck[1] - ampthck[0] ) / ampthck[2] )+1
        jdv = np.int( ( phsthck[1] - phsthck[0] ) / phsthck[2] )+1

        tr = PolarAxes.PolarTransform()
        degree_ticks = lambda d: (d*np.pi/180, "%d$^\\circ$"%(d))
        angle_ticks = map(degree_ticks, np.linspace(phsthck[0],phsthck[1],jdv))
        grid_locator1 = GF.FixedLocator([v for v, s in angle_ticks])
        tick_formatter1 = GF.DictFormatter(dict(angle_ticks))

        STDgrid = np.arange(ampthck[0],ampthck[1]+0.00001,ampthck[2])
        tick_formatter2 = GF.DictFormatter(dict(zip(STDgrid,map(str,STDgrid))))
        grid_locator2 = GF.FixedLocator(STDgrid)

        phspi=phsrange/180*np.pi
        gh = FA.GridHelperCurveLinear(tr,
             extremes=(phspi[0], phspi[1], amprange[0],amprange[1]),
             grid_locator1=grid_locator1,
             grid_locator2=grid_locator2,
             tick_formatter1=tick_formatter1,
             tick_formatter2=tick_formatter2)
#                               extremes=(-np.pi/4.*1, np.pi/4.*1, smin, smax),

#       fig = plt.figure(figsize=(8,6))
        ax = FA.FloatingSubplot(fig, rect, grid_helper=gh)
        fig.add_subplot(ax)
    
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text(phstitle)
        ax.axis["bottom"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["bottom"].toggle(ticklabels=False, label=False)
        ax.axis["right"].set_axis_direction("left") # "X axis"
        ax.axis["right"].toggle(ticklabels=True, label=True)
        ax.axis["right"].label.set_text(amptitle)
        ax.axis["left"].set_axis_direction("bottom") # "X axis"
        ax.axis["left"].toggle(ticklabels=False, label=False)
#       ax.grid(color='0.7')
        ax.grid(color='dimgray', linewidth =1.5 )
    def add_contours(self, levs=[0.1,0.2,0.3],  **kwargs):
        piphi=np.pi/180.*self.phsrange
        rs,ts=np.meshgrid( np.linspace(self.amprange[0],self.amprange[1],num=100), np.linspace(piphi[0],piphi[1],num=100) )
        rms = np.sqrt( ( self.reff)**2 + rs**2 -2*(self.reff)*rs*np.cos(ts))
        contours = plt.contour(rs*np.cos(ts),rs*np.sin(ts),rms,levels=levs,**kwargs)
        
        return contours

if __name__=='__main__':
#
    cal=np.zeros((4))+[10.80-5.03j, 8.44-5.40j, 6.84-4.10j, 8.71-4.83j]
    obs=np.zeros((4))+[14.78-0.45j,12.89-0.27j,11.21-0.14j,12.93-0.00j]
    rat=cal/obs

    smin=5.0
    smax=15
    swdt=2.5
    tmin=-40.
    tmax=20.
    twdt=10.
    aaa=' M2_amplitude'
    bbb='phase lag'
    refft=np.abs(obs[3])
    
    arng=np.array((smin-0.5,smax+0.5))
    prng=np.array((tmin-2.0,tmax+2.0))
    athc=np.array((smin,smax,swdt))
    pthc=np.array((tmin,tmax,twdt))
    
    fig = plt.figure(figsize=(8,6))
    dia = AmpPhsDiagram(reff=refft,fig=fig,amprange=arng,ampthck=athc,phsrange=prng,phsthck=pthc,amptitle=aaa,phstitle=bbb)
    contours=dia.add_contours(levs=[2.5,5.0,7.5],colors='0.5')
    plt.clabel(contours, inline=1, fontsize=10,fmt="%.1f")
    #plt.scatter(1,0,marker='*',s=70)
    plt.scatter(obs[0:4].real,obs[0:4].imag,marker='s', s=40, color='orange',label='Obs.')
    plt.scatter(obs[3].real,obs[3].imag,marker='s', s=42, color='orange',edgecolor='black')
    plt.scatter(cal[0:4].real,cal[0:4].imag,marker='o', s=40, color='white',edgecolor='dodgerblue',label='Cal.')
    plt.legend(loc="lower left",ncol=3,scatterpoints=1)
    plt.savefig('test_orig.png')
    plt.show()

    smin=0.5
    smax=1.5
    swdt=0.25
    tmin=-30.
    tmax=30
    twdt=15
    aaa='ratio of M2_amplitude(cal/obs)'
    bbb='phase lag'
    refft=1.0
 
    arng=np.array((smin-0.10,smax+0.1))
    prng=np.array((tmin-5.00,tmax+5.0))
    athc=np.array((smin,smax,swdt))
    pthc=np.array((tmin,tmax,twdt))

    fig = plt.figure(figsize=(8,6))
    dia = AmpPhsDiagram(reff=refft,fig=fig,amprange=arng,ampthck=athc,phsrange=prng,phsthck=pthc,amptitle=aaa,phstitle=bbb)
    contours=dia.add_contours(levs=[0.1,0.2,0.3],colors='0.5')
    plt.clabel(contours, inline=1, fontsize=10,fmt="%.1f")

    plt.savefig('test_ratio.png')
    plt.show()
   

