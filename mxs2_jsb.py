#!/usr/bin/env python

import math

from numpy import mean, var

import jsbsim
from pymap3d.ned import geodetic2ned, ned2geodetic


def ft2m(ft):
    return ft*0.3048

def m2ft(m):
    return m/0.3048

def deg2rad(deg):
    return deg/180.0 * math.pi

def rad2deg(rad):
    return rad/math.pi * 180.0

CARTESIAN_ORIGIN=(deg2rad(51.4125),deg2rad(-2.5645),0)

def get_imperial_state(fdm):
    lat = fdm["position/lat-gc-rad"]
    lon = fdm["position/long-gc-rad"]
    h = fdm["position/geod-alt-ft"]
    
    u = fdm["velocities/u-fps"]
    v = fdm["velocities/v-fps"]
    w = fdm["velocities/w-fps"]
    
    # roll = rad2deg(fdm["attitude/phi-rad"])
    # pitch = rad2deg(fdm["attitude/theta-rad"])
    # yaw = rad2deg(fdm["attitude/psi-rad"])
    roll = fdm["attitude/phi-rad"]
    pitch = fdm["attitude/theta-rad"]
    yaw = fdm["attitude/psi-rad"]
    
    p = fdm["velocities/p-rad_sec"]
    q = fdm["velocities/q-rad_sec"]
    r = fdm["velocities/r-rad_sec"]
    
    return [lat,lon,h,u,v,w,roll,pitch,yaw,p,q,r]


def get_geodetic_state(fdm):
    lat = fdm["position/lat-gc-rad"]
    lon = fdm["position/long-gc-rad"]
    h = ft2m(fdm["position/geod-alt-ft"])
    
    u = ft2m(fdm["velocities/u-fps"])
    v = ft2m(fdm["velocities/v-fps"])
    w = ft2m(fdm["velocities/w-fps"])
    
    roll = rad2deg(fdm["attitude/phi-rad"])
    pitch = rad2deg(fdm["attitude/theta-rad"])
    yaw = rad2deg(fdm["attitude/psi-rad"])
    
    p = fdm["velocities/p-rad_sec"]
    q = fdm["velocities/q-rad_sec"]
    r = fdm["velocities/r-rad_sec"]
    
    return [lat,lon,h,u,v,w,roll,pitch,yaw,p,q,r]

def get_metric_state(fdm):
    lat = fdm["position/lat-gc-rad"]
    lon = fdm["position/long-gc-rad"]
    h = ft2m(fdm["position/geod-alt-ft"])
    [x,y,z] = geodetic2ned(lat,lon,h,*CARTESIAN_ORIGIN,deg=False)
    
    u = ft2m(fdm["velocities/u-fps"])
    v = ft2m(fdm["velocities/v-fps"])
    w = ft2m(fdm["velocities/w-fps"])
    
    roll = rad2deg(fdm["attitude/phi-rad"])
    pitch = rad2deg(fdm["attitude/theta-rad"])
    yaw = rad2deg(fdm["attitude/psi-rad"])
    
    p = fdm["velocities/p-rad_sec"]
    q = fdm["velocities/q-rad_sec"]
    r = fdm["velocities/r-rad_sec"]
    
    return [x,y,z,u,v,w,roll,pitch,yaw,p,q,r]


def set_initial_state(fdm,state):
    [x,y,z,u,v,w,roll,pitch,yaw,p,q,r] = state
    
    [lat,lon,h] = ned2geodetic(x,y,z,*CARTESIAN_ORIGIN,deg=False)
    
    fdm["ic/lat-gc-rad"] = lat
    fdm["ic/long-gc-rad"] = lon
    fdm["ic/h-sl-ft"] = m2ft(h) # Not really...
    
    fdm["ic/phi-rad"] = roll
    fdm["ic/theta-rad"] = pitch
    fdm["ic/psi-true-rad"] = yaw
    
    fdm["ic/u-fps"] = m2ft(u)
    fdm["ic/v-fps"] = m2ft(v)
    fdm["ic/w-fps"] = m2ft(w)
    
    fdm["ic/p-rad_sec"] = p
    fdm["ic/q-rad_sec"] = q
    fdm["ic/r-rad_sec"] = r


def sensible(array):
    elements = ", ".join([f"{v:.4f}" for v in array])
    return f"[{elements}]"

fdm = jsbsim.FGFDMExec(".")
fdm.load_model("mxs2")
set_initial_state(fdm,[0,0,-500, 13,0,0, 0,0,0, 0,0,0])


scale = 1
deltaT = 0.01/scale
fdm.set_dt(deltaT)

print(sensible(get_metric_state(fdm)))

import sys
import time

outfile = None
if len(sys.argv) > 1:
    outfile = open(sys.argv[1],"w")
    outfile.write("time,x,y,z,u,v,w,roll,pitch,yaw,p,q,r\n")

samples = 1
sample_times = []

for i in range(samples):
    count = 0
    simtime = 0
    
    fdm.run_ic()
    
    start = time.process_time()
    while count < 6000*scale:
        fdm.run()
        # moment = fdm["aero/qbar-pa"]* fdm["metrics/Sw-sqm"]* fdm["metrics/cbarw-m"]* fdm["aero/function/c_m_alpha"]
        # print(f"Alpha: {fdm['aero/alpha-rad']:.3f}, q: {fdm['aero/qbar-pa']:.3f}, alpha_q: {fdm['aero/function/alpha_q-rad']:.3f}, c_m: {fdm['aero/function/c_m_alpha']:.3f}, moment: {moment:.3f}")
        count += 1
        simtime += deltaT
        if outfile:
            # pass
            # get_imperial_state(fdm)
            # get_geodetic_state(fdm)
            # get_metric_state(fdm)
            outfile.write(f"{simtime},"+sensible(get_metric_state(fdm))[1:-1] + "\n")
    end = time.process_time()
    sample_times.append(end-start)
    print(sensible(get_metric_state(fdm)))

print(f"Mean: {mean(sample_times)}\nVar: {var(sample_times)}")
outfile.close()