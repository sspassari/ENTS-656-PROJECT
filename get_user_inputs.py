# -*- coding: utf-8 -*-
"""
Created on Mon May 13 13:19:26 2019

@author: Soumyaa
"""

def get_time():
    user_input=4
    try:
        user_input=int(input("Enter the simulation time in hours :"))  
    except ValueError:
        print("not a valid input")
    return user_input

def get_distance():
    distance=12
    try:
         distance=int(input("Enter the distance between the two base stations in km"))
    except ValueError:
        print("not a valid input")
    return distance

def get_users():
    users=1000
    try:
         users=int(input("Enter the number of users"))
    except ValueError:
        print("not a valid input")
    return users

def get_speed():
    speed=15
    try:
        speed=int(input("Enter speed in m/s"))
    except ValueError:
        print("not a valid input")
    return speed

