# -*- coding: utf-8 -*-
"""
Created on Wed May  8 10:41:52 2019

@author: Soumyaa
"""
#from time import time, sleep
import numpy as np




distance_from_bstn=[]
#num_users = 1000 #take user input
dist_bw_bstns=12
user_location=0
current_user_location=0


def get_user_location(num_users):
    user_location=np.random.uniform(0.0,12.0,size=num_users)
    current_user_location=np.random.randint(0,num_users)
    return user_location[current_user_location]

#1 signifies right to left 0 signifies left to right
def get_user_direction(location):
    if location < dist_bw_bstns/2: 
        return 0
    else:
       return 1
def update_user_location(u):
    if u.direction is 0 :
        if u.location <12:
            u.location+=0.015
        elif u.location>11.999:
            u.flag=True
    elif u.direction is 1: 
        if u.location>0:
            u.location-=0.015
        elif u.location<0.001:
            u.flag=True
    
        
    


    
    
        