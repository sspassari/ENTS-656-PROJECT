# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:10:25 2019

@author: Soumyaa
"""

#import userlocation as ul
import numpy as np
from collections import Counter
import userlocation as ul
import user

num_total_users_attempting_calls=0
#num_users=1000 #take user input
users=[]

def getCallProbability():
    user_call_rate_lambda=1
    call_probability=user_call_rate_lambda/3600
    return call_probability

def get_users_attempting_call(users_currently_active_attempting,num_users):
    call_probability=getCallProbability()
    elements=[1,0]
    weights=[call_probability,1-call_probability]
    user_span=num_users-users_currently_active_attempting
    attempting_users=np.random.choice(elements, size=user_span,p=weights)
    number_users_attempting_call=Counter(attempting_users)[1]
    return number_users_attempting_call
    
def assign_locations(num_users):
    location=ul.get_user_location(num_users)
    direction=ul.get_user_direction(location)
    user_id=num_total_users_attempting_calls
    curr_user=user.user(user_id,location,direction)
    return curr_user
    #return [user_id,location,direction]
    
def get_call_duration():
    duration=np.random.exponential(180)
    return duration

def update_call_duration(u):
    u.current_duration+=1
    

    