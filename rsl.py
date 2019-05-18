# -*- coding: utf-8 -*-
"""
Created on Thu May  9 06:18:22 2019

@author: Soumyaa
"""
import math
import numpy as np
rsl=0
fr=1000
height_antenna=50
height_mobile=1.7
shadow_res=10
EIRP=55
fading=[]
rsl_thresh=-102
def get_okh(distance):
    okh=69.55+26.16*math.log10(fr)-13.82*math.log10(height_antenna)+(44.9-6.55*math.log10(height_antenna))*math.log10(distance)-(1.1*math.log10(fr)-0.7)*height_mobile+(1.56*math.log10(fr)-0.8)
    return okh

def get_fading():
    fading= 20*math.log10(np.random.rayleigh())
    return fading

def  compute_shadowing(dist):
     shadow=np.random.normal(0,2,dist*100)
     return shadow
 
def get_shadow(shadow,dist):
    return shadow[int(dist*100)]

def get_rsl(shadow,dist):
    rsl=EIRP-get_okh(dist)+get_fading()+get_shadow(shadow,dist)
    return rsl
    
def get_choice(rsl1,rsl2):
    choice=0
   
        
    return choice
    

get_fading()